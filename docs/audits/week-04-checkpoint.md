# Current completion audit — Week 4

**Incomplete: 24/72 instructional chapters are authored and validated.** Weeks
1–4 have separate week/day chapters, 24 independent labs with runnable starters
and separate references, four weekly examinations and two cumulative phase
defenses. Days 25–72, later assessments, and integrated ForgeAgent remain unfinished.
The [manifest](../build-progress.json) records exact continuation state.

New Week 4 code implements deterministic toy BPE, a complete one-block causal
decoder using our scalar autograd, learned content/positions, multiple attention
heads, per-token normalization, residuals, ReLU FFN, stable cross-entropy, finite
CPU training, sampling and a correctness-tested KV cache. It deliberately omits
optional biases/gains/dropout and uses inefficient scalar Python objects. Toy
pattern loss is not described as language quality or coding-agent competence.

Executed: 42 tests passed locally on Python 3.12.16 and 3.14.4, all 24 authored Python
lesson blocks ran, all 24 lab references passed, local file links and checkpoint
integrity passed, and compileall succeeded. Tests verify numerical parameter
and loss gradients, causal value/gradient independence, cached/full equivalence,
context limits and sampling support. New Week 4 tests have not yet run remotely
at this pre-publication checkpoint. [Evidence](../validation-results.json) retains
previous runs separately; historical test counts are not current totals.

Week 3 was committed/pushed as one weekly commit, `76eb2c5`, and its
[remote CI](https://github.com/sdivyanshu90/agent-engineering-from-scratch/actions/runs/44083228939)
completed successfully. The workflow checks Python 3.12, 3.13 and 3.14 on Ubuntu.
The earlier 115 individually pushed files and the user's revised one-commit-per-
week policy are recorded in [publication history](../publication-history.json).
No force push/history rewrite occurred. Historical audits for
[Phase 1](../audits/phase-01-checkpoint.md) and [Week 3](../audits/week-03-checkpoint.md)
preserve their own dates/scopes rather than implying those older statements are
current. Windows and macOS execution remain untested.

Author review checked representation boundaries, projection/head dimensions,
normalization axes/epsilon, causal eligibility before softmax, shifted targets,
stable loss derivatives, the 176-parameter toy count, sampling filter order and
cache ownership. Important simplifications differ explicitly from the original
transformer paper. Twenty-six primary page URLs are in the resource ledger,
including the original paper's full HTML and versioned attention reference.
No installed PyTorch dependency or November 2026 provider compatibility is claimed.
Independent technical review and beginner usability testing remain outstanding.

Limitations: no model provider/application integration, retrieval/RAG, agent
runtime, durable agent events/context, MCP/Skills/A2A, controlled patches, command
sandbox, agent benchmark, production telemetry/API or container yet. The earlier
HTTP transport remains a local learning subset; pathname checks are not OS
isolation, and thread-backed writes may outlive caller cancellation. The scalar
learning code is CPU-sized and has recursion/performance/numerical-domain limits.
The cache stores Value graphs for visibility and is not a memory-efficient
production cache. No live or paid model calls, stochastic agent results or
production deployment were performed.

The full-completion gate must still fail: 48 lessons and later deliverables are
absent. Next: research Week 5's model-provider boundaries, typed output and
streaming/recovery, author its six complete lessons/labs, validate and publish
one weekly commit, then continue through Week 12. Never replace missing chapters
with topic summaries to claim completion.
