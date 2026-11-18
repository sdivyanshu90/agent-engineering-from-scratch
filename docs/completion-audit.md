# Completion audit

The November 18 integration checkpoint covers 72 separate instructional days,
12 weekly reviews and exams, six cumulative phase exams and a final technical
defense. The [roadmap](../ROADMAP.md) orders the material.
The [coverage matrix](concept-coverage-matrix.md) links each lesson to its
concepts, lab, reference and assessment.

## Verified

| Check | Evidence |
|---|---|
| Strict curriculum integrity | 72/72 chapters, each with 20 required sections and a diagram, executable example, and lab and assessment mapping |
| Reference lab contracts | 72 pass with deterministic local inputs |
| Full code suite | 123 tests pass on Linux/Python 3.12.15 with the pinned schema/service extras |
| Local Markdown | No unresolved file paths; this validator checks file targets only |
| Linux execution | Generated test passed after the reviewed fixture update; separate namespace smoke tested environment, mounts, network and read-only workspace |
| Container | Digest-pinned build and locked dependencies; ephemeral API smoke passed authenticating, enqueueing and returning a revision-bound citation |
| Agent benchmark | 11/11 development, 6/6 frozen visible held-out scripted cases; case-level data and denominators committed |
| Weekly publication | Weeks 7–11 independently staged, tested, pushed and confirmed green in GitHub Actions; final Week 12 verification uses the same workflow |

## Pedagogical and implementation review

Foundation chapters introduce the terminal and object state before HTTP.
Vector arithmetic, derivatives and normalization precede the toy decoder.
Storage ownership, typed contracts and retry semantics precede the agent
runtime. Provenance and authorization precede MCP discovery, then reappear in
the workload, queue and approval paths. Auditing surfaced three inline
examples that depended on undeclared state and six Week 10 chapters without
executable snippets. These now run as standalone examples from the root.
The strict validator checks structure. Learner readability, conceptual mastery
and retention require the rubrics, changed-fixture exercises and defenses.

Week 12 keeps a single-host educational boundary. The hosted provider and
container are optional. MCP implements a pinned stdio tools subset; Skills
frontmatter is intentionally restricted; A2A is taught conceptually.
Human patch approval runs in the local host. The API exposes read-only
evidence collection. The Linux backend was tested on owned fixtures.
Windows and macOS, live stochastic coding quality, true model spend and
multi-tenant production operations were outside the executed checks.
Visible held-out data must be replaced for a genuinely blind external study.

See [numerical results](validation-results.json),
[benchmark rows](agent-benchmark-results.json),
[resource verification](resource-verification.md),
and the [capstone limitations](../projects/forgeagent/LIMITATIONS.md).
