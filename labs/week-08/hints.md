# Week 8 hints

Validate the entire DAG before returning a single ready layer. A deterministic
tie rule makes plans reviewable, but does not make two effects safe to parallelize.
Reserve policy/system context first; calculate one documented heuristic and
label it an estimate. Drop stale memory before ranking. Stable sorting needs a
final identity tie-breaker.

Compaction should tell the reader that content was dropped and retain references
to the source revisions. Do not promote a model-generated summary to trusted
policy. `BEGIN IMMEDIATE` plus revision comparison can serialize local writers;
keep the transaction short. A local database transaction cannot include a remote
payment or email. Persist intent before an effect and result after it; recovery
must distinguish pending/unknown from complete and ask the external system or an
operator to reconcile ambiguity.
