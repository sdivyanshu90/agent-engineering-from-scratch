"""Public, deterministic minimum contracts for the Week 12 labs."""
import argparse
import importlib.util
from pathlib import Path

NAMES = ['search', 'trajectory', 'approval', 'execution', 'resume', 'benchmark']

def load(path):
    spec = importlib.util.spec_from_file_location('submission', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

ROOT = Path(__file__).resolve().parents[2]


def check(day, path=None):
    m = load(path or ROOT / "solutions/labs/week-12" / (NAMES[day - 1] + ".py"))
    if day == 1:
        hits = m.search_sources({'b.py':'other\nadd item', 'a.py':'add item'}, 'add')
        assert [x['path'] for x in hits] == ['a.py', 'b.py']
        assert hits[1]['line'] == 2
        assert m.search_sources({'x':'nothing'}, 'missing') == []
    elif day == 2:
        events = [{'event':'patch_proposed','proposal_id':'p','review_sha256':'h','after_sha256':'r'},
                  {'event':'patch_approved','proposal_id':'p','review_sha256':'h','approved':True},
                  {'event':'patch_applied','proposal_id':'p','revision':'r'},
                  {'event':'tests_end','revision':'r','status':'passed'}]
        assert m.repair_is_verified(events)
        assert not m.repair_is_verified(events[:-1])
    elif day == 3:
        assert m.review_digest('x', 'before', 'after') == m.review_digest('x', 'before', 'after')
        assert m.review_digest('x', 'before', 'after') != m.review_digest('y', 'before', 'after')
    elif day == 4:
        class Executor:
            def run(self, argv, *, cwd, timeout):
                assert argv == ('python', '-m', 'unittest', 'discover', '-s', 'tests')
                assert cwd == 'fixture' and timeout == 30
                return {'status':'passed'}
        assert m.run_fixed_tests(Executor(), 'fixture', 'python')['status'] == 'passed'
    elif day == 5:
        assert m.recover_snapshot({'n':1}, 1, [{'revision':2,'kind':'agent_snapshot','payload':{'snapshot':{'n':2}}}]) == {'revision':2,'state':{'n':2}}
    elif day == 6:
        summary = m.summarize([{'id':'a','split':'dev','solved':True}, {'id':'b','split':'dev','solved':False}, {'id':'c','split':'heldout','solved':True}], 'dev')
        assert summary['denominator'] == 2 and summary['solved'] == 1 and summary['rate'] == .5

    return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--day', type=int, choices=range(1, 7), required=True)
    parser.add_argument('--module', type=Path)
    args = parser.parse_args()
    check(args.day, args.module)
    print('Public contract passed:', NAMES[args.day - 1])
