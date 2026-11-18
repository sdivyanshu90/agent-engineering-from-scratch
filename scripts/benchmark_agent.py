#!/usr/bin/env python3
"""Run the frozen local Agent fixture benchmark; no network or live model."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from forgeagent.evaluation import evaluate,load_fixture,wilson

MANIFEST=ROOT/'docs/week-10-manifest.json'

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--split',choices=['dev','heldout'],default='dev')
    parser.add_argument('--final-evaluation',action='store_true',help='explicitly authorize one heldout evaluation run')
    args=parser.parse_args()
    if args.split=='heldout' and not args.final_evaluation:
        parser.error('heldout requires --final-evaluation; do not tune against this split')
    manifest=json.loads(MANIFEST.read_text())
    path=ROOT/manifest['fixtures'][args.split]['path']
    digest=hashlib.sha256(path.read_bytes()).hexdigest()
    if digest!=manifest['fixtures'][args.split]['sha256']:
        raise SystemExit('fixture hash differs from frozen Week 10 manifest')
    report=evaluate(load_fixture(path),split=args.split)
    report['fixture_sha256']=digest
    report['wilson_95_percent_interval']=wilson(report['passed'],report['case_count']) if report['case_count'] else None
    print(json.dumps(report,indent=2,sort_keys=True))

if __name__=='__main__':main()
