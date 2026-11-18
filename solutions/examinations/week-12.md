# Week 12 reference criteria

The capstone has three distinct paths: model-visible observation/proposal
tools, human-only approval, and trusted fixed test execution through an injected
backend. A correct submission never registers approval or apply as a provider
tool. Proposal identity binds session, tool, arguments, path, source revision,
and replacement digest; apply rechecks the source and consumes one use.

A trajectory is accepted only when its ordered events bind one proposal to a
matching approval, apply at the proposal's after digest, and a passing test at
that same digest. A finish answer alone is insufficient. The test executor must
fail closed without a backend, and a fake backend result must be labeled as
adapter fixture evidence only.

Durable recovery includes typed runtime messages, counters, observations,
pending calls, deadline, and tool identity. A full snapshot event can recover
the append/checkpoint gap. Restored proposals are unapproved. Apply intent is
resolved by before/after file hash and operation state; an ambiguous tree stays
unknown for human reconciliation.

Evaluation reports every fixed case and split denominator. Scripted provider
fixtures demonstrate protocol mechanics only; visible data is not an
independent estimate of deployment quality. A strong defense names assumptions
about filesystem races, runner isolation, identities, retrieval coverage,
context loss, and benchmark contamination. The exact numeric score depends on
the submission and must be computed from observed evidence, never supplied in
advance.
