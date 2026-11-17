import argparse
from dataclasses import asdict
import importlib.util
import json
import math
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
NAMES={1:'chunks',2:'sparse',3:'dense',4:'fusion',5:'metrics',6:'support'}


def load_module(path):
    spec=importlib.util.spec_from_file_location('week06_submission',path)
    module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module)
    return module


def rejects(function):
    try:function()
    except ValueError:return
    raise AssertionError('invalid input accepted')


def check(day,path=None):
    module=load_module(path or ROOT/'solutions/labs/week-06'/(NAMES[day]+'.py'))
    from forgeagent.retrieval import chunk_text
    if day==1:
        text='a\nb\nc\nd\ne\n';chunks=module.split_document('p',text,3,1)
        assert [(c.start_line,c.end_line) for c in chunks]==[(1,3),(3,5)]
        assert chunks[0].text=='a\nb\nc\n'
        assert chunks==module.split_document('p',text,3,1)
        assert module.split_document('p','')==[]
        rejects(lambda:module.split_document('p',text,3,3))
    elif day==2:
        chunks=chunk_text('a','agent agent')+chunk_text('b','tests tests')
        result=module.rank('AGENT',chunks,1)
        assert result[0].identifier==chunks[0].identifier
        assert math.isclose(result[0].score,math.log(2)*1.375)
        assert module.rank('unknown',chunks)==[]
        rejects(lambda:module.rank('x',chunks,-1))
    elif day==3:
        vectors={'near':[-.01,1],'far':[1,0]};query=[.01,1]
        assert module.nearest(vectors,query,1)[0].identifier=='near'
        assert module.nearest(vectors,query,1,True)[0].identifier=='far'
        rejects(lambda:module.nearest({'x':[0,0]},query))
    elif day==4:
        result=module.combine([['x','y'],['y','z']],60,3)
        assert [r.identifier for r in result]==['y','x','z']
        assert math.isclose(result[0].score,1/61+1/62)
        rejects(lambda:module.combine([['x','x']]))
    elif day==5:
        result=module.metrics(['b','x','a'],{'a':2,'b':1},3)
        assert math.isclose(result['precision'],2/3) and result['recall']==1
        assert math.isclose(result['ndcg'],2.5/(3+1/math.log2(3)))
        assert module.metrics([],{},1)['ndcg']==0
        rejects(lambda:module.metrics(['a','a'],{'a':1}))
    else:
        chunks=chunk_text('p','Evidence.');c=chunks[0]
        value={'answer':'Evidence.','citations':[{'chunk_id':c.identifier,'revision':c.revision,'quote':'Evidence.'}]}
        assert not module.supported(json.dumps(value),chunks).abstained
        value['answer']='Evidence. Extra claim.'
        rejects(lambda:module.supported(json.dumps(value),chunks))
        assert module.supported('{"answer":"Insufficient evidence.","citations":[]}',chunks).abstained
    return True


if __name__=='__main__':
    sys.path.insert(0,str(ROOT));parser=argparse.ArgumentParser()
    parser.add_argument('--day',type=int,choices=NAMES,required=True);parser.add_argument('--module',type=Path)
    args=parser.parse_args();check(args.day,args.module);print(f'Week 6 day {args.day}: public contract passed')
