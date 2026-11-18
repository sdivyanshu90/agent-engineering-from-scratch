# ForgeAgent design decisions

## D1 — Keep the model-facing tool set narrow

Use registered search/read/propose/test tools rather than a shell. The
tradeoff is less flexibility; the benefit is that each effect has a reviewable
handler and fixed schema. Future tools require a separate capability review.

## D2 — Treat proposal as a write-gated request, not an applied change

The runtime's write gate protects proposal creation, while the registry does
not contain approval or apply. The caller explicitly enables the proposal tool.
The human callback must inspect the full exact replacement. A digest binds the
review but does not authenticate the reviewer.

## D3 — Bind patch to bytes and consume once

The workspace binds session, tool arguments, path, original hash, and
replacement hash. Apply rechecks current bytes and consumes one approval. The
implementation assumes an owned, non-adversarial workspace and does not claim
race-proof symlink safety.

## D4 — Inject test execution and fail closed

No backend means no execution. A fixed argv removes model-controlled command
construction. The injected backend owns OS isolation, process-tree cleanup,
resource limits, filesystem/network policy, and result provenance. A recording
fake only tests adapter behavior.

## D5 — Persist full snapshots around pending decisions

Full snapshots are simple to validate and recover but can grow. A snapshot event
repairs the append/checkpoint gap. Proposal receipts restore unapproved. External
effects use operation intents and file-hash reconciliation; a local journal
does not create exactly-once execution across arbitrary systems.

## D6 — Prefer transparent fixtures over proxy claims

Scripted provider decisions make protocol behavior deterministic and
inspectable. We report them as protocol regression, not held-out coding skill.
Fixed visible cases support reproducible checks but limit external validity.
