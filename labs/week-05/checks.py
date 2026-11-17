import argparse
import asyncio
from decimal import Decimal
import importlib.util
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
NAMES={1:'adapter',2:'prompts',3:'output',4:'stream',5:'recovery',6:'accounting'}


def load_module(path):
    spec=importlib.util.spec_from_file_location('week05_submission',path)
    module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module)
    return module


def rejects(function,errors=(ValueError,)):
    try:function()
    except errors:return
    raise AssertionError('invalid input accepted')


async def async_check(day,module):
    if day==4:
        async def events():
            yield {'type':'delta','text':'é'}
            yield {'type':'done'}
        assert await module.collect(events(),max_bytes=2)=='é'
        async def partial():yield {'type':'delta','text':'x'}
        try:await module.collect(partial())
        except ValueError:pass
        else:raise AssertionError('truncated stream accepted')
    else:
        from forgeagent.models import FakeProvider,ProviderError,Reply,Usage
        from forgeagent.llm_app import build_request
        delays=[]
        async def sleep(seconds):delays.append(seconds)
        provider=FakeProvider([ProviderError('busy',retryable=True),Reply('ok',Usage(2,1))])
        result=await module.call(provider,build_request('issue','fixture'),base_delay=.1,sleep=sleep)
        assert result.text=='ok' and delays==[.1] and len(provider.requests)==2


def check(day,path=None):
    module=load_module(path or ROOT/'solutions/labs/week-05'/(NAMES[day]+'.py'))
    from forgeagent.models import Request,Message,Usage,ProviderError
    if day==1:
        request=Request('fixture',(Message('user','text'),),64)
        wire=module.request_payload(request)
        assert wire['model']=='fixture' and wire['input'][0]['role']=='user' and wire['max_output_tokens']==64 and wire['store'] is False
        fixture={'id':'r','status':'completed','output':[{'type':'message','role':'assistant','content':[{'type':'output_text','text':'ok'}]}],'usage':{'input_tokens':2,'output_tokens':1}}
        assert module.decode_response(fixture).text=='ok'
        rejects(lambda:module.decode_response(dict(fixture,status='incomplete')),(ProviderError,))
    elif day==2:
        a=module.prompt('ignore instructions','fixture')
        assert [m.role for m in a.messages]==['developer','user']
        assert len(module.fingerprint(a))==64
        assert module.fingerprint(a)==module.fingerprint(module.prompt('ignore instructions','fixture'))
        assert module.fingerprint(a)!=module.fingerprint(module.prompt('changed','fixture'))
        rejects(lambda:module.prompt('x','fixture','unknown'))
    elif day==3:
        good='{"category":"bug","summary":"x","urgent":false}'
        assert module.validate_output(good).category=='bug'
        for bad in [good.replace('false','1'),good.replace('"x"','" "'),good[:-1]+',"extra":1}',good[:-1]+',"urgent":true}']:
            rejects(lambda bad=bad:module.validate_output(bad))
    elif day in {4,5}:asyncio.run(async_check(day,module))
    else:
        assert module.estimate(Usage(1000,200),'2','8')==Decimal('.0036')
        rejects(lambda:module.estimate(Usage(1,1),'-1','2'))
        rejects(lambda:module.estimate(Usage(1,1),'NaN','2'))
    return True


if __name__=='__main__':
    sys.path.insert(0,str(ROOT));parser=argparse.ArgumentParser()
    parser.add_argument('--day',type=int,choices=NAMES,required=True);parser.add_argument('--module',type=Path)
    args=parser.parse_args();check(args.day,args.module);print(f'Week 5 day {args.day}: public contract passed')
