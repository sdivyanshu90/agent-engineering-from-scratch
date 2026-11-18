def validate(arguments,schema):
    if not isinstance(arguments,dict) or schema.get('type')!='object' or schema.get('additionalProperties') is not False: raise ValueError('closed object required')
    props=schema.get('properties',{}); required=schema.get('required',[])
    if set(arguments)-set(props) or not set(required)<=set(arguments): raise ValueError('argument keys')
    out={}
    for key,value in arguments.items():
        spec=props[key]; kind=spec.get('type')
        ok={'string':isinstance(value,str),'integer':type(value) is int,'boolean':type(value) is bool}.get(kind,False)
        if not ok: raise ValueError('argument type')
        if kind=='string' and len(value.encode())>spec.get('maxLength',4096): raise ValueError('argument length')
        if kind=='integer' and not spec.get('minimum',-10**6)<=value<=spec.get('maximum',10**6): raise ValueError('argument range')
        if 'enum' in spec and value not in spec['enum']: raise ValueError('argument enum')
        out[key]=value
    return out
