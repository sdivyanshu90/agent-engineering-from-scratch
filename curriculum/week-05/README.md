# Week 5 — Reliable LLM application engineering

Prerequisite: [Phase 2 defense](../../assessments/phase-examinations/phase-02.md).
Build a model boundary that can be tested independently from a hosted model.

| Day | Chapter | Independent artifact |
|---|---|---|
| 1 / D25 | [Providers and lifecycle](day-01/README.md) | Typed-to-wire adapter |
| 2 / D26 | [Messages and prompt identity](day-02/README.md) | Role-preserving prompt/fingerprint |
| 3 / D27 | [Structured validation](day-03/README.md) | Strict parser and optional Pydantic comparison |
| 4 / D28 | [Streaming and cancellation](day-04/README.md) | Terminal-state stream assembly |
| 5 / D29 | [Recovery, limits and routing](day-05/README.md) | Classified finite retry/deadline |
| 6 / D30 | [Usage and evaluation](day-06/README.md) | Unit-safe cost and honest quality report |

Use [labs](../../labs/week-05/README.md), [review](weekly-review.md) and
[exam](../../assessments/weekly/week-05.md). Budget 42–54 focused hours; extend
when gates fail. Ordinary code uses only the standard library and supplied
responses. Pydantic is an optional pinned schemas extra. Live inference is optional,
requires explicit opt-in/key/configured model and may incur charges; it is never
required to pass ordinary tests. The current live adapter is nonstreaming, while
normalized stream assembly is independently tested.
