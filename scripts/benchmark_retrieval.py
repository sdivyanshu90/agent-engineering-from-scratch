"""Run the fixed visible teaching benchmark; no external calls or tuning."""
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from forgeagent.grounding import benchmark

if __name__=='__main__':
    fixture=json.loads((ROOT/'datasets/evaluation-fixtures/retrieval.json').read_text())
    print(json.dumps(benchmark(fixture),indent=2))
