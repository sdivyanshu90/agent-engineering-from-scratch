import argparse
import importlib.util
import math
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
NAMES={1:'route_comparison',2:'intervals',3:'redaction',4:'fixture_integrity',5:'calibration',6:'boundary_audit'}
def load(path):
    spec=importlib.util.spec_from_file_location('week10_submission',path);mod=importlib.util.module_from_spec(spec);sys.modules[spec.name]=mod;spec.loader.exec_module(mod);return mod
def check(day,path=None):
    m=load(path or ROOT/'solutions/labs/week-10'/(NAMES[day]+'.py'))
    if day==1:
        r=m.compare([{'route':'a','passed':True,'seconds':1,'cost_usd':.2},{'route':'a','passed':False,'seconds':3,'cost_usd':.4}])['a']
        assert r['n']==2 and r['pass_rate']==.5 and math.isclose(r['mean_seconds'],2) and math.isclose(r['mean_cost_usd'],.3)
    elif day==2:
        lo,hi=m.wilson(4,4);assert 0<lo<1 and hi==1
    elif day==3:
        assert m.redact({'event':'tool_start','prompt':'sensitive','tool':'secret','step':2})=={'event':'tool_start','step':2}
    elif day==4:assert m.verify(b'fixture',''.join(__import__('hashlib').sha256(b'fixture').hexdigest()))
    elif day==5:assert m.agreement([{'human':'yes','score':'yes'},{'human':'no','score':'yes'}])==.5
    else:assert m.assess({'status':'failed','effects':0}) and not m.assess({'status':'failed','effects':1})
    return True
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--day',type=int,choices=NAMES,required=True);p.add_argument('--module',type=Path);a=p.parse_args();sys.path.insert(0,str(ROOT));check(a.day,a.module);print(f'Week 10 day {a.day}: public contract passed')
