# Week 10 review

Freeze the run configuration and verify the development fixture digest before
starting. Run the development benchmark twice and compare ordered case outcomes,
token counts, and elapsed time separately. Explain why timing differs and why
repeated scripted decisions do not estimate live model reliability.

Take the [weekly exam](../../assessments/weekly/week-10.md) independently. Rebuild
one expected event sequence and predict how the grader reacts when an otherwise
successful run performs a forbidden action. Then compare your reasoning with
the [reference](../../solutions/examinations/week-10.md).

| Symptom | Remediation |
|---|---|
| Every plausible answer passes | Add an observable task postcondition and an insufficient-evidence case. |
| A parser failure looks like injection resistance | Trace the boundary actually exercised and add a case reaching policy dispatch. |
| Successful calls hide failed trajectories | Keep every attempt and reason in the fixed denominator. |
| A trace contains raw source text | Rebuild the export allowlist and test that unrelated identifiers and inputs stay out. |

Proceed to the [cumulative assessment](../../assessments/phase-examinations/phase-05.md)
after reproducing one failure and its corrected result on a changed development
fixture. Reserve the fixed evaluation split for the frozen implementation.
