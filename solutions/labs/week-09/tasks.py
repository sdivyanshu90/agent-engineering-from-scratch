import hashlib, json, re

def parse_tool_result(result):
    if not isinstance(result,dict) or type(result.get('isError')) is not bool or not isinstance(result.get('content'),list): raise ValueError('malformed result')
    if result['isError']: return None
    texts=[part['text'] for part in result['content'] if isinstance(part,dict) and part.get('type')=='text' and isinstance(part.get('text'),str)]
    return '\n'.join(texts)
def normalize_skill_name(value):
    if not isinstance(value,str): raise ValueError('name')
    name=value.strip().lower()
    if len(name)>64 or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',name): raise ValueError('name')
    return name
def patch_binding(session,tool,arguments,revision):
    if not all(isinstance(x,str) and x for x in (session,tool,revision)) or not isinstance(arguments,dict): raise ValueError('binding')
    return hashlib.sha256(json.dumps([session,tool,arguments,revision],sort_keys=True,separators=(',',':')).encode()).hexdigest()
def validate_manifest(card):
    if not isinstance(card,dict) or set(card)!={'name','skills','capabilities'}: raise ValueError('fields')
    if not isinstance(card['name'],str) or not re.fullmatch(r'[a-z][a-z0-9-]{0,62}',card['name']): raise ValueError('name')
    for key in ('skills','capabilities'):
        values=card[key]
        if not isinstance(values,list) or any(not isinstance(v,str) or not v for v in values) or len(set(values))!=len(values): raise ValueError(key)
    return True
def content_hash(data):
    if not isinstance(data,bytes): raise ValueError('bytes required')
    return hashlib.sha256(data).hexdigest()
def authorized_tool(name,allowlist):
    return isinstance(name,str) and name in allowlist
