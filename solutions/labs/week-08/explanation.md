# Week 8 reference reasoning

The implementation is split into pure planning/context operations and a file
backed event journal. A DAG planner validates all dependency references and
cycles before a caller can act. It emits stable topological layers; this is a
plan, not permission to run unsafe effects concurrently. Verification recomputes
the expected plan, so a modified order cannot silently masquerade as valid.

Context items carry role, provenance, trust class, source revision, creation time
and optional TTL. Selection drops expired items, reserves caller-specified
high-authority instructions, then orders evidence by lexical overlap, trust,
recency and stable ID. It charges UTF-8 bytes at roughly four bytes per token.
That reproducible estimate helps compare policies; it is not an exact tokenizer
and must not replace provider usage reconciliation. Compaction truncates and
retains references/revisions while marking its text as derived and untrusted.

The SQLite journal makes the revision compare-and-append atomic within one local
database transaction. Owner and session are part of every key. Checkpoints store
JSON snapshots with an expected revision; resume returns the snapshot and later
event tail. The separate operation table binds an operation ID to a canonical
payload digest. Intent, external effect and result recording are distinct steps.
If a process dies after a remote effect but before result recording, the local
status cannot establish whether the effect occurred. `unknown` is a required
reconciliation state, not a retry signal.

Run `python labs/week-08/checks.py --day N` for each day. The reference code uses
only the standard library. It is educational: it does not supply distributed
consensus, encryption, retention policy, remote idempotency semantics or a model
tokenizer.
