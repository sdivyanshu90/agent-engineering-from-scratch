"""MCP 2025-11-25 stdio server for two harmless demonstration tools."""
import json
import sys

VERSION='2025-11-25'
MAX_LINE=1_000_000
TOOLS=[{'name':'echo','description':'Return the supplied text.','inputSchema':{'type':'object','properties':{'text':{'type':'string'}},'required':['text'],'additionalProperties':False}}, {'name':'add','description':'Add two integers.','inputSchema':{'type':'object','properties':{'a':{'type':'integer'},'b':{'type':'integer'}},'required':['a','b'],'additionalProperties':False}}]


def serve(inp=None,out=None):
    inp=inp or sys.stdin.buffer; out=out or sys.stdout.buffer
    state='new'
    for raw in inp:
        if len(raw)>MAX_LINE or not raw.endswith(b'\n'): return 2
        try:
            def pairs(items):
                result={}
                for key,value in items:
                    if key in result: raise ValueError('duplicate key')
                    result[key]=value
                return result
            msg=json.loads(raw.decode('utf-8'),object_pairs_hook=pairs,parse_constant=lambda _: (_ for _ in ()).throw(ValueError('nonfinite')))
            if not isinstance(msg,dict) or msg.get('jsonrpc')!='2.0' or not isinstance(msg.get('method'),str): raise ValueError
        except (ValueError,UnicodeDecodeError): return 2
        method=msg['method']; ident=msg.get('id'); params=msg.get('params',{})
        if 'id' in msg and (isinstance(ident,bool) or not isinstance(ident,(str,int))): return 2
        if not isinstance(params,dict):
            if 'id' in msg:
                out.write((json.dumps({'jsonrpc':'2.0','id':ident,'error':{'code':-32602,'message':'params must be object'}})+'\n').encode());out.flush();continue
            return 2
        def reply(value):
            out.write((json.dumps(value,separators=(',',':'),ensure_ascii=False)+'\n').encode()); out.flush()
        if method=='initialize' and state=='new' and 'id' in msg:
            reply({'jsonrpc':'2.0','id':ident,'result':{'protocolVersion':VERSION,'capabilities':{'tools':{}},'serverInfo':{'name':'forgeagent-demo','version':'1.0.0'}}}); state='await_initialized'
        elif method=='notifications/initialized' and state=='await_initialized' and 'id' not in msg: state='ready'
        elif method=='tools/list' and state=='ready' and 'id' in msg:
            reply({'jsonrpc':'2.0','id':ident,'result':{'tools':TOOLS}})
        elif method=='tools/call' and state=='ready' and 'id' in msg:
            name=params.get('name'); args=params.get('arguments')
            if name=='echo' and isinstance(args,dict) and set(args)=={'text'} and isinstance(args['text'],str): value=args['text']
            elif name=='add' and isinstance(args,dict) and set(args)=={'a','b'} and all(type(args[k]) is int for k in ('a','b')): value=str(args['a']+args['b'])
            else: reply({'jsonrpc':'2.0','id':ident,'result':{'content':[{'type':'text','text':'invalid tool or arguments'}],'isError':True}}); continue
            reply({'jsonrpc':'2.0','id':ident,'result':{'content':[{'type':'text','text':value}],'isError':False}})
        elif method=='exit' and state=='ready' and 'id' not in msg: return 0
        else:
            if 'id' in msg: reply({'jsonrpc':'2.0','id':ident,'error':{'code':-32600,'message':'invalid request or lifecycle state'}})
            else: return 2
    return 0

if __name__=='__main__': raise SystemExit(serve())
