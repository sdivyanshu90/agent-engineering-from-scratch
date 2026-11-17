# Week 2 independent labs

Work under `learner-work/week-02/`. Copy the relevant runnable starter. The
baseline returns a result but does not satisfy the exercise; failing learner
checks are expected until you implement it. Reference code is separate.

| Local day / global ID | Starter | Input/output and acceptance |
|---|---|---|
| 1 / D07 | [validation.py](starter/validation.py) | `validate_document(bytes) -> str`; UTF-8 JSON, exactly one string text field, ≤4096 body bytes and ≤2000 text code points; reject duplicates, non-finite extensions, malformed shape, encoding, excess length with ValueError/UnicodeError. |
| 2 / D08 | [storage.py](starter/storage.py) | `Store(path)` with put(owner,id,text) and get(owner,id); persist across instances, composite ownership key, parameterized values, empty string distinct from missing None; transaction rollback and close evidence required. |
| 3 / D09 | [concurrent.py](starter/concurrent.py) | `async collect(operations)` starts zero-argument async operations concurrently; return input-ordered results, [] for empty, propagate failure and clean up siblings. |
| 4 / D10 | [recovery.py](starter/recovery.py) | `async retry(operation, attempts=3, timeout=1.0, base_delay=.05, sleep=...)`; retry only exported TransientError, finite attempt/delay settings, exact backoff, no trailing sleep, timeout/permanent errors/cancellation propagate. |
| 5 / D11 | [vectors.py](starter/vectors.py) | dot, cosine, matvec on moderate finite numeric vectors; require equal nonempty dimensions, reject zero cosine, rectangular row shapes; no NumPy. |
| 6 / D12 | [optimization.py](starter/optimization.py) | central derivative (positive finite h); stable softmax on nonempty finite logits; square descent with 0<rate<1, nonnegative integer steps and history including initial x. |

Run `python labs/week-02/checks.py --day 1` to check the reference. Add
`--module learner-work/week-02/validation.py` to test your own implementation;
select other local day numbers for the corresponding contract. Run all reference
contracts with `python scripts/validate_exercises.py`. Repository tests include
additional async and API integration cases and must not require paid calls.

Submit source, tests, predicted/observed traces, one deliberately reproduced
failure, and a tradeoff paragraph. For async tests use events or injected sleep
rather than exact timing. For database tests use temporary files, not production
state. The transport demonstration is bounded localhost teaching code; never
expose it as an Internet service. Grading and hand-calculation questions are in
[the weekly assessment](../../assessments/weekly/week-02.md).
