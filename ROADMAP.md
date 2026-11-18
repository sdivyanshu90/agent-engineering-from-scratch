# How to follow the program

**Begin now:** [setup](START_HERE.md) → [diagnostic](assessments/diagnostic/README.md)
→ [Week 1](curriculum/week-01/README.md). Days are separate documents under
`curriculum/week-NN/day-NN/README.md`. Read them in order; pass the gate before
following the next link. Week numbering is the whole-program number, 01–12.
Day numbering restarts at 01 each week. The unique global identifier D01–D72
is recorded in the manifest, so Week 2 / Day 1 is D07.

```mermaid
flowchart TD
  A[Setup and diagnostic] --> B[Weeks 1–2: Python, software, mathematics]
  B --> C[Weeks 3–4: learning, autograd, transformers]
  C --> D[Weeks 5–6: model integration and grounded retrieval]
  D --> E[Weeks 7–8: runtime, context, durable state]
  E --> F[Weeks 9–10: interoperability, security, evaluation]
  F --> G[Weeks 11–12: service infrastructure and ForgeAgent defense]
```

Use the table to open each available week.

| Week | Build toward | Exit evidence | Availability |
|---|---|---|---|
| 1 | Local document-search CLI | Correct counts, stable search, visible failures, tests | [Ready checkpoint](curriculum/week-01/README.md) |
| 2 | Async storage-backed API and math routines | Transactions, cancellation, vector/derivative traces | [Ready checkpoint](curriculum/week-02/README.md) |
| 3 | Mini-autograd and tiny neural models | Analytic versus numerical gradients, honest evaluation scope | [Available](curriculum/week-03/README.md) |
| 4 | Tiny decoder transformer | Shape/mask tests and reproducible CPU generation | [Available](curriculum/week-04/README.md) |
| 5 | Reliable model adapter | Typed outputs, bounded retries, streaming/cancellation tests | [Available](curriculum/week-05/README.md) |
| 6 | Retrieval and grounded answers | Fixed queries, relevance metrics, citation checks | [Available](curriculum/week-06/README.md) |
| 7 | Framework-free runtime | Tool validation, transitions, stopping budgets | [Available](curriculum/week-07/README.md) |
| 8 | Resumable context-aware runtime | Crash/restart, idempotency, provenance and memory tests | [Available](curriculum/week-08/README.md) |
| 9 | MCP and constrained execution | Negotiation, discovery, denied-operation tests | [Available](curriculum/week-09/README.md) |
| 10 | Reliability/security benchmark | Frozen grading, adversarial tasks, repeated-trial results | [Available](curriculum/week-10/README.md) |
| 11 | Authenticated service | Ownership, workers, telemetry, container recovery | [Available](curriculum/week-11/README.md) |
| 12 | Integrated ForgeAgent | Functional/adversarial benchmark and technical defense | [Available](curriculum/week-12/README.md) |

## A normal instructional day

Allocate 45 minutes to closed-book recall and prerequisite checks, 90 minutes
to the chapter and hand traces, 75 minutes to reconstructing the worked example,
120 minutes to the independent lab, 60 minutes to experiments/debugging, and
60 minutes to the exam and notes. This is 7.5 focused hours; take breaks outside
those blocks. It is a suggested budget, not a measured requirement. If you
cannot explain the result, extend the session or add another day. Do not skip
remediation to preserve a calendar.

On the seventh day, perform the weekly review, take the exam independently,
inspect reference solutions afterward, and reconstruct failed mechanisms from
their contracts. Recheck one previous week's skill without looking at it.
Take a cumulative exam after each two-week phase. The week overview links to each available exam.
The intended learning levels and evidence are in [COMPETENCY_FRAMEWORK](COMPETENCY_FRAMEWORK.md).

## When to move, skip, or pause

Move when the day's explicit implementation, explanation, and exam gates pass.
Skip only by producing equivalent unseen-input evidence from the diagnostic;
vocabulary recognition is insufficient. Pause for remediation when your code
passes public checks but you cannot trace why it works.

Complete beginners may need 1–3 extra weeks on Python, 1–2 on engineering/math,
and 2–4 on ML/transformer foundations. These are estimates and are not guarantees
of either minimum or maximum time. Assess demonstrated competence continuously.
