# Initial curriculum audit

## Input and scope

The only source curriculum available is the twelve-week specification in the
request. The workspace's original README had no lessons or implementation.
There is no separate earlier roadmap to compare. Specialization: reliable AI
agent systems engineering from first principles. The scope excludes unrelated
computer vision, reinforcement-learning training systems, and model-scale
pretraining infrastructure.

## Prerequisite repairs

A beginner cannot jump directly from Python syntax to HTTP services. Week 1
therefore teaches terminal working directories, files versus processes, values,
control flow, functions, collections, exceptions, modules, objects, tests, and
Git before the CLI milestone. Week 2 introduces byte/text encodings, network
messages, timeouts, validation, and ownership before asynchronous storage APIs.
A schema checks shape; authorization checks permission. Teach these separately.

Vectors precede embeddings. Derivatives precede backpropagation. Probabilities
and logarithms precede cross-entropy. Matrix shapes precede attention. Plain
loops and state transitions precede agent runtimes. Local file safety precedes
exposing filesystem tools. Tool observations are untrusted data from their
first introduction, not a security topic deferred to Week 10.

## Load and extensions

Six days is extremely compressed for a first programming language. Reserve
an extra 1–3 weeks after Week 1 if the learner cannot reconstruct the CLI or
read tracebacks independently. Week 2 combines software engineering and math;
reserve another 1–2 weeks for vector/derivative remediation. Weeks 3–4 may need
2–4 extra weeks for learners without algebra fluency. These are planning
estimates, not measured completion times. The 12-week route is an intensive
minimum planning scaffold, not a promise of competence on a deadline.

## Work remaining

Days 25–72 still need substantive chapters, independent labs, solutions, code,
and tests. The graph is initially a conservative sequential dependency chain;
minimal skip-enabling prerequisite edges must be audited as chapters are authored.
No automatic validator can establish teaching depth or mathematical correctness.
