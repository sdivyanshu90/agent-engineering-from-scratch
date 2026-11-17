import argparse
import importlib.util
import math
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
NAMES={1:'bpe',2:'projections',3:'attention',4:'normalization',5:'loss',6:'sampling'}


def load_module(path):
    spec=importlib.util.spec_from_file_location('week04_submission',path)
    module=importlib.util.module_from_spec(spec)
    sys.modules[spec.name]=module
    spec.loader.exec_module(module)
    return module


def rejects(function):
    try:function()
    except ValueError:return
    raise AssertionError('invalid input accepted')


def check(day,path=None):
    module=load_module(path or ROOT/'solutions/labs/week-04'/(NAMES[day]+'.py'))
    if day==1:
        source=['a','a','a']
        assert module.merge(source,('a','a'))==['aa','a'] and source==['a','a','a']
        assert module.encode('abab',[('a','b'),('ab','ab')])==['abab']
        assert ''.join(module.encode(' café! ',[('a','f')]))==' café! '
    elif day==2:
        q,k,v=module.project([1,0],[0,1],[[1,0],[0,2]],[[0,1],[1,0]],[[1,1],[1,-1]])
        assert q==[1,2] and k==[1,1] and v==[2,0]
        rejects(lambda:module.project([1],[0,1],[[1]],[[1]],[[1]]))
    elif day==3:
        result=module.attend([1],[[0],[1]],[[2],[6]])
        assert math.isclose(result[0],(2+6*math.e)/(1+math.e))
        assert module.attend([1],[[1000]],[[9]])==[9]
        rejects(lambda:module.attend([1],[],[]))
        rejects(lambda:module.attend([1,2],[[1]],[[2]]))
    elif day==4:
        result=module.layer_norm([1,3])
        assert math.isclose(result[0],-1/math.sqrt(1.00001))
        assert module.layer_norm([2,2])==[0,0]
        rejects(lambda:module.layer_norm([]))
        rejects(lambda:module.layer_norm([1,2],epsilon=0))
        rejects(lambda:module.layer_norm([float('nan')]))
    elif day==5:
        assert math.isclose(module.loss([1000,1001],1),math.log1p(math.exp(-1)))
        assert math.isclose(module.loss([0,0],0),math.log(2))
        rejects(lambda:module.loss([],0))
        rejects(lambda:module.loss([0,1],2))
    else:
        assert module.choose([0,1,2],temperature=0)==2
        assert module.choose([0,1,2],top_k=1)==2
        assert module.choose([0,0],temperature=0)==0
        assert module.choose([0,1],seed=7)==module.choose([0,1],seed=7)
        rejects(lambda:module.choose([0],temperature=-1))
        rejects(lambda:module.choose([0],top_p=0))
        rejects(lambda:module.choose([0],top_k=2))
    return True


if __name__=='__main__':
    sys.path.insert(0,str(ROOT))
    parser=argparse.ArgumentParser()
    parser.add_argument('--day',type=int,choices=NAMES,required=True)
    parser.add_argument('--module',type=Path)
    args=parser.parse_args()
    check(args.day,args.module)
    print(f'Week 4 day {args.day}: public contract passed')
