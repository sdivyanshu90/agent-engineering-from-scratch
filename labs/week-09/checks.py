"""Week 9 deterministic public contract checks; no network required."""
import argparse, importlib.util, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
NAMES={1:'tasks',2:'tasks',3:'tasks',4:'tasks',5:'tasks',6:'tasks'}
def load(path):
    spec=importlib.util.spec_from_file_location('week09_submission',path); m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m);return m
def check(day,path=None):
    m=load(path or ROOT/'solutions/labs/week-09/tasks.py')
    if day==1:
        assert m.parse_tool_result({'content':[{'type':'text','text':'ok'}],'isError':False})=='ok'
        assert m.parse_tool_result({'content':[{'type':'text','text':'bad'}],'isError':True}) is None
    elif day==2:
        assert m.normalize_skill_name('  Summarize-Logs ')=='summarize-logs'
        for x in ('../escape','two words','--bad'):
            try:m.normalize_skill_name(x)
            except ValueError:pass
            else:raise AssertionError('invalid name accepted')
    elif day==3:
        one=m.patch_binding('s','edit',{'path':'a'},'abc'); assert one==m.patch_binding('s','edit',{'path':'a'},'abc')
        assert one!=m.patch_binding('other','edit',{'path':'a'},'abc')
    elif day==4:
        assert m.validate_manifest({'name':'worker','skills':['read'],'capabilities':['text']})
        for x in ({'name':'../bad','skills':[],'capabilities':[]},{'name':'worker','skills':['x','x'],'capabilities':[]}):
            try:m.validate_manifest(x)
            except ValueError:pass
            else:raise AssertionError('invalid manifest accepted')
    elif day==5:
        assert m.content_hash(b'abc')=='ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad'
        assert m.content_hash(b'')=='e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
    else:
        assert m.authorized_tool('read_file',{'read_file'})
        assert not m.authorized_tool('shell',{'read_file'})
    return True
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--day',type=int,choices=NAMES,required=True);p.add_argument('--module',type=Path);a=p.parse_args();sys.path.insert(0,str(ROOT));check(a.day,a.module);print(f'Week 9 day {a.day}: public contract passed')
