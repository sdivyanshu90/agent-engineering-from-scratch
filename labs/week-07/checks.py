"""Public contracts for Week 7; these checks are not a substitute for review."""
import argparse, importlib.util, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def load(path):
    spec=importlib.util.spec_from_file_location('week07_submission',path)
    module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module);return module
def rejects(fn):
    try: fn()
    except (ValueError,TypeError): return
    raise AssertionError('invalid input accepted')
def check(day,path=None):
    if day not in range(1,7): raise ValueError('day must be 1..6')
    m=load(path or ROOT/'solutions/labs/week-07'/f'day{day:02}.py')
    if day==1:
        assert m.route('fixed: invoice',.9)=={'mode':'workflow','state':'PARSE'}
        assert m.route('ambiguous',.9)['mode']=='agent' and m.route('fixed: x',.2)['state']=='REVIEW'
        rejects(lambda:m.route('x',2))
    elif day==2:
        s={'type':'object','properties':{'id':{'type':'integer','minimum':1,'maximum':9},'tag':{'type':'string','maxLength':4}},'required':['id'],'additionalProperties':False}
        assert m.validate({'id':3,'tag':'ok'},s)=={'id':3,'tag':'ok'}
        rejects(lambda:m.validate({'id':True},s));rejects(lambda:m.validate({'id':2,'extra':1},s));rejects(lambda:m.validate({},s))
    elif day==3:
        called=[]; tools={'add':lambda x:x+1}
        status,obs=m.run(['{"type":"calls","calls":[{"name":"add","arguments":{"x":2}}]}','{"type":"finish","answer":"three"}'],tools)
        assert status=='completed' and obs==[{'ok':True,'result':3}]
        status,obs=m.run(['{"type":"calls","calls":[{"name":"add","arguments":{"x":2}},{"name":"missing","arguments":{}}]}'],tools)
        assert status=='failed' and obs==[]
    elif day==4:
        assert m.layers([('a',[]),('b',[]),('c',['a'])])==[['a','b'],['c']]
        rejects(lambda:m.layers([('a',['z'])]));rejects(lambda:m.layers([('a',['b']),('b',['a'])]))
    elif day==5:
        assert m.reconcile(7,5,10)=={'used':12,'overshot':True,'may_continue':False}
        assert m.reconcile(7,2,10)['may_continue']
        rejects(lambda:m.reconcile(-1,2,10))
    else:
        r=m.summarize([{'event':'model_start'},{'event':'failure','code':'bad_protocol'},{'event':'run_end','status':'failed'}])
        assert r['status']=='failed' and r['failures']==['bad_protocol'] and r['counts']['model_start']==1
        rejects(lambda:m.summarize([None]))
    return True
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--day',type=int,choices=range(1,7),required=True);p.add_argument('--module',type=Path);a=p.parse_args();sys.path.insert(0,str(ROOT));check(a.day,a.module);print(f'Week 7 day {a.day}: public contract passed')
