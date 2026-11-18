import argparse, importlib.util, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
FILES={1:'workflow.py',2:'workflow.py',3:'context.py',4:'context.py',5:'journal.py',6:'journal.py'}
def load(path):
    spec=importlib.util.spec_from_file_location('week08_submission',path);m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m);return m
def rejects(fn):
    try: fn()
    except (ValueError,KeyError): return
    raise AssertionError('invalid input accepted')
def check(day,path=None):
    path=path or ROOT/'solutions/labs/week-08'/FILES[day];m=load(path)
    if day in (1,2):
        from forgeagent.durable import Step
        steps=[Step('a'),Step('b',('a',)),Step('c',('a',))]
        if day==1:
            result=m.plan(steps)
            assert [[s.identifier for s in layer] for layer in result]==[['a'],['b','c']]
            rejects(lambda:m.plan([Step('a',('z',))]))
            rejects(lambda:m.plan([Step('a',('b',)),Step('b',('a',))]))
        else:
            result=m.plan(steps);assert m.verify(steps,result)
            rejects(lambda:m.verify(steps,[result[1],result[0]]))
            decision=m.evaluate('digest-v1',[{'name':'parse','passed':True,'evidence':'fixture:a'},{'name':'roundtrip','passed':False,'evidence':'fixture:b'}],{'parse','roundtrip'},1)
            assert decision['status']=='revise' and decision['failures']==['roundtrip']
            rejects(lambda:m.evaluate('x',[],{'required'},2))
    elif day==3:
        from forgeagent.context import ContextItem
        a=ContextItem('a','alpha context','user','chat','verified','r1',1,10)
        b=ContextItem('b','alpha evidence','tool','tool','untrusted','r2',9)
        stale=ContextItem('old','alpha stale','user','memory','verified','r0',1,1)
        result=m.select([a,b,stale],'alpha',20,now=5)
        assert stale not in result and result[0].identifier=='a'
        assert m.estimate_tokens('abcd')==1
    elif day==4:
        from forgeagent.context import ContextItem
        x=ContextItem('source','a substantially longer source text that exceeds the output bound','user','file','verified','rev',1)
        summary=m.compact([x],max_chars=24)
        assert summary.lossy and summary.source_refs==('source',) and summary.source_revisions==('rev',)
        assert len(summary.text)<=24 and 'TRUNCATED' in summary.text and 'untrusted' in summary.authority
    elif day==5:
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            j=m.Journal(Path(d)/'db.sqlite');assert j.append('o','s',0,'x',{'n':1})==1
            rejects(lambda:j.append('o','s',0,'x',{}))
            assert j.revision('other','s')==0
    else:
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            j=m.Journal(Path(d)/'db.sqlite');r=j.append('o','s',0,'counter',{'n':2})
            j.checkpoint('o','s','c',{'count':2},r);assert j.resume('o','s','c')['state']=={'count':2}
    return True
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--day',type=int,choices=FILES,required=True);p.add_argument('--module',type=Path);a=p.parse_args();sys.path.insert(0,str(ROOT));check(a.day,a.module);print(f'Week 8 day {a.day}: public contract passed')
