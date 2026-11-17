"""Public Week 3 contracts; default references, --module selects learner code."""
import argparse
import importlib.util
import math
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[2]
NAMES={1:"partition",2:"regression",3:"network",4:"scalar",5:"optimizer",6:"bigram"}


def load_module(path):
    spec=importlib.util.spec_from_file_location("week03_submission",path)
    module=importlib.util.module_from_spec(spec)
    sys.modules[spec.name]=module
    spec.loader.exec_module(module)
    return module


def rejects(function):
    try: function()
    except ValueError: return
    raise AssertionError("invalid input accepted")


def check(day,path=None):
    module=load_module(path or ROOT/"solutions/labs/week-03"/(NAMES[day]+".py"))
    if day==1:
        from forgeagent.learning import Example
        rows=[Example(str(i),(float(i),),float(i)) for i in range(10)]
        result=module.partition(rows)
        assert [len(result[k]) for k in ['train','validation','test']]==[6,2,2]
        assert sorted(row.identifier for values in result.values() for row in values)==[str(i) for i in range(10)]
        assert result==module.partition(rows)
        assert rows[0].identifier=='0'
        rejects(lambda:module.partition(rows[:3]))
        rejects(lambda:module.partition(rows+[rows[0]]))
    elif day==2:
        w,b=module.step([1,2],[3,5],0,0,0.1)
        assert math.isclose(w,1.3) and math.isclose(b,0.8)
        rejects(lambda:module.step([],[],0,0))
    elif day==3:
        assert module.forward([1,2],[[1,-1],[0,2]],[0,-1],[[2,1]],[.5])==[3.5]
        rejects(lambda:module.forward([1,2],[[1]],[0],[[1]],[0]))
    elif day==4:
        x=module.Scalar(3)
        a=x*x
        y=a+a+x
        y.backward()
        assert y.data==21 and x.grad==13
        y.backward()
        assert x.grad==13
        z=2*x+1
        z.backward()
        assert x.grad==2
    elif day==5:
        from forgeagent.autograd import Value
        p=Value(2);p.grad=3
        module.update([p],.1)
        assert math.isclose(p.data,1.7) and p.grad==3
        rejects(lambda:module.update([p,p],.1))
        rejects(lambda:module.update([p],-1))
    else:
        result=module.distribution('abab','ab','a',1)
        assert result=={'a':.25,'b':.75}
        assert module.distribution('','ab','a',1)=={'a':.5,'b':.5}
        rejects(lambda:module.distribution('abc','ab','a',1))
        rejects(lambda:module.distribution('ab','ab','a',0))
    return True


if __name__=='__main__':
    sys.path.insert(0,str(ROOT))
    parser=argparse.ArgumentParser()
    parser.add_argument('--day',type=int,choices=NAMES,required=True)
    parser.add_argument('--module',type=Path)
    args=parser.parse_args()
    check(args.day,args.module)
    print(f'Week 3 day {args.day}: public contract passed')
