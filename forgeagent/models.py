"""Week 5 model boundary: typed requests, deterministic fakes, optional HTTP adapter.

No live call occurs on import or in ordinary tests. Pricing is supplied by the
caller; this module contains no claims about current model prices.
"""
import asyncio
from dataclasses import asdict,dataclass
from decimal import Decimal,InvalidOperation
import hashlib
import json
import math
from typing import Protocol
import urllib.error
import urllib.request


class ProviderError(Exception):
    def __init__(self, code, *, retryable=False):
        super().__init__(code)
        self.code,self.retryable=code,retryable


@dataclass(frozen=True)
class Message:
    role: str
    content: str
    def __post_init__(self):
        if self.role not in {'system','developer','user','assistant'} or not isinstance(self.content,str):
            raise ValueError('invalid message role/content')


@dataclass(frozen=True)
class Request:
    model: str
    messages: tuple[Message,...]
    max_output_tokens: int=256
    prompt_version: str='v1'
    def __post_init__(self):
        if not isinstance(self.model,str) or not self.model or not self.messages or not isinstance(self.messages,tuple):
            raise ValueError('model and nonempty immutable message tuple required')
        if any(not isinstance(message,Message) for message in self.messages):
            raise ValueError('typed messages required')
        if type(self.max_output_tokens) is not int or not 1<=self.max_output_tokens<=8192:
            raise ValueError('output allowance must be integer 1..8192')

    def fingerprint(self):
        canonical=json.dumps(asdict(self),sort_keys=True,ensure_ascii=False,separators=(',',':'))
        return hashlib.sha256(canonical.encode()).hexdigest()


@dataclass(frozen=True)
class Usage:
    input_tokens: int
    output_tokens: int
    def __post_init__(self):
        if any(type(value) is not int or value<0 for value in (self.input_tokens,self.output_tokens)):
            raise ValueError('nonnegative integer usage required')


@dataclass(frozen=True)
class Reply:
    text: str
    usage: Usage
    response_id: str='fixture'


class Provider(Protocol):
    async def complete(self,request: Request) -> Reply: ...


class FakeProvider:
    def __init__(self,outcomes):
        self.outcomes=list(outcomes)
        self.requests=[]
    async def complete(self,request):
        self.requests.append(request)
        await asyncio.sleep(0)
        if not self.outcomes:
            raise ProviderError('fixture_exhausted')
        outcome=self.outcomes.pop(0)
        if isinstance(outcome,Exception):raise outcome
        if not isinstance(outcome,Reply):raise ProviderError('invalid_fixture_reply')
        return outcome


def payload(request):
    return {'model':request.model,'input':[asdict(m) for m in request.messages],
            'max_output_tokens':request.max_output_tokens,'store':False}


def parse_response(value):
    if not isinstance(value,dict) or value.get('status')!='completed':
        raise ProviderError('response_incomplete')
    texts=[]
    output=value.get('output')
    if not isinstance(output,list):raise ProviderError('response_shape')
    for item in output:
        if not isinstance(item,dict):raise ProviderError('response_shape')
        if item.get('type')=='reasoning':continue
        if item.get('type')!='message' or item.get('role')!='assistant':
            raise ProviderError('unsupported_output_item')
        if not isinstance(item.get('content'),list):raise ProviderError('response_shape')
        for part in item['content']:
            if not isinstance(part,dict):raise ProviderError('response_shape')
            if part.get('type')=='refusal':raise ProviderError('refusal')
            if part.get('type')!='output_text' or not isinstance(part.get('text'),str):
                raise ProviderError('unsupported_content')
            texts.append(part['text'])
    usage=value.get('usage')
    if not texts or not isinstance(usage,dict) or not isinstance(value.get('id'),str):
        raise ProviderError('response_shape')
    try:counts=Usage(usage['input_tokens'],usage['output_tokens'])
    except (KeyError,ValueError):raise ProviderError('usage_shape') from None
    return Reply(''.join(texts),counts,value['id'])


class OpenAIResponses:
    """Minimal nonstreaming Responses adapter; requires explicit live opt-in.

    The default transport uses HTTPS, bounded response bytes and socket timeout.
    It rejects tools/non-text outputs instead of silently dropping them. A socket
    timeout is not a total deadline; cancellation cannot stop a running worker.
    """
    def __init__(self,key,*,allow_live=False,timeout=10.0,transport=None):
        if not math.isfinite(timeout) or timeout<=0:raise ValueError('positive finite timeout required')
        if transport is None and (not allow_live or not key):
            raise ValueError('explicit allow_live and key required for real HTTP')
        self.key,self.timeout=key,timeout
        self.transport=transport or self._post

    def _post(self,body):
        request=urllib.request.Request('https://api.openai.com/v1/responses',
            data=json.dumps(body).encode(),headers={'Authorization':'Bearer '+self.key,'Content-Type':'application/json'},method='POST')
        class NoRedirect(urllib.request.HTTPRedirectHandler):
            def redirect_request(self,*args,**kwargs):
                raise ProviderError('redirect_not_allowed')
        try:
            opener=urllib.request.build_opener(NoRedirect())
            with opener.open(request,timeout=self.timeout) as response:
                raw=response.read(1_000_001)
                if len(raw)>1_000_000:raise ProviderError('response_too_large')
                return json.loads(raw)
        except urllib.error.HTTPError as error:
            raise ProviderError(f'http_{error.code}',retryable=error.code in {429,500,502,503,504}) from None
        except (urllib.error.URLError,TimeoutError):
            # Outcome/billing may be uncertain; do not mark as automatically retryable.
            raise ProviderError('transport_uncertain') from None
        except (ValueError,UnicodeError):raise ProviderError('invalid_response_json') from None

    async def complete(self,request):
        return parse_response(await asyncio.to_thread(self.transport,payload(request)))


def cost(usage,input_per_million,output_per_million):
    try:rates=[Decimal(str(input_per_million)),Decimal(str(output_per_million))]
    except InvalidOperation:raise ValueError('numeric rates required') from None
    if any(not rate.is_finite() or rate<0 for rate in rates):raise ValueError('finite nonnegative rates required')
    return (usage.input_tokens*rates[0]+usage.output_tokens*rates[1])/Decimal(1_000_000)
