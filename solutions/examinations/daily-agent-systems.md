# Daily examination checkpoints, Weeks 8–12

Attempt each examination independently. Use each answer to check the rationale
and reconstruct the lab with new inputs. The individual chapter's rubric
takes precedence. Where it gives no point split, award one point each for
correct explanation, a trace, an implementation, a diagnosis, and a defensible
design choice. Verify the implementation with the linked public lab and an
unseen counterexample.

## Week 8

- **D43.** Initial indegree zero gives `[A,B]`, then `[C]`, then `[D]`.
  `B,A,C,D` is valid. Reject unknown dependency IDs before dispatch. Stable
  traversal orders work selection but a handler can depend on clocks or
  external state. Move a cyclic verification or retry into a separately
  budgeted transition when the dependency truly spans iterations.
- **D44.** An unknown mandatory criterion cannot produce acceptance. Stop as
  indeterminate or obtain new evidence within budget. Bind judgments to
  candidate and rubric versions. One agent can inspect correctness while a
  separate worker runs checks; the coordinator rejects incomplete evidence
  and routes conflicts to a reviewer. Shared examples create correlated error.
- **D45.** Reject expired items before ranking, reserve instruction capacity
  first, then consume candidate capacity using the documented byte estimate.
  Duplicates are invalid input. Tool text cannot acquire a privileged role by
  naming one. Synonyms can be missed and repeated terms can inflate relevance.
  Compare versioned selectors on held-fixed queries and cited evidence.
- **D46.** A suffix negation is lost if it lies beyond the truncation point.
  Reserve explicit decision fields and source IDs, revisions and authority.
  TTL is a time filter, while revision checks freshness against the source.
  Serialize the compact record and its lineage together at a known revision.
- **D47.** Compare expected/current revision, increment and append in one
  transaction. One concurrent writer at expected 5 succeeds at 6 and the
  second sees a conflict. Resume at checkpoint 8 and apply events 9 then 10.
  Use a different owner with a known session ID as a negative case. Version
  the payload and migrate only after checking invariants.
- **D48.** Before intent, no durable request exists. After intent and before
  response, effect status may be unknown. After local receipt it is resolved.
  Bind a stable key to owner, session, operation and canonical arguments;
  reject same-key/different-content reuse. Query remote status if supported.
  Otherwise preserve uncertainty for review. SQLite cannot commit remote state.

## Week 9

- **D49.** The mismatched response ID is the first failure. Close the connection
  and skip tools/list. Negotiate only host-supported capabilities and authorize
  reads independently. A tool-level error is in a valid response result;
  a JSON-RPC error describes failure at the protocol/request layer.
- **D50.** The late frame can be mistaken for the next reply unless the client
  matches IDs. The teaching client closes on timeout. Enumerated tools still
  require local allowlist and argument checks. Stdio stdout is protocol data;
  send diagnostics to stderr.
- **D51.** An exact digest match supports byte-level current equality within
  the digest assumption. It cannot prove the file was never changed.
  Path, tool, arguments and session are separate approval inputs. File
  descriptors rooted in a protected directory and an isolated mount can bound
  races that a previous comparison or hash cannot prevent.
- **D52.** Valid required fields are metadata. The local loader deliberately
  restricts optional frontmatter; unsupported fields cannot register tools.
  Treat accepted body text as untrusted context. Reject parent components
  before opening references. A committed file can still come from an
  untrusted change and carries no host authority.
- **D53.** Deny the private folder because consent covers public data only.
  Query or subscribe to the task using the task ID. Artifact text is data.
  A2A tasks have a separate lifecycle, while the taught MCP subset returns
  an observation from a synchronous tool call.
- **D54.** Filter descriptions by capability before constructing the prompt,
  obtain approval from the trusted UI, recheck exact source bytes at apply,
  and delegate tests to an isolation backend. Retain policy verdict, operation
  identity, digests, status and duration with reviewed metadata.

## Week 10

- **D55.** The side-effect case scores zero, with 19/20 total passing. A correct
  textual answer cannot compensate for an unauthorized effect. Freeze the
  expected trace and authorization checks before running the fixture.
- **D56.** TP=TN=FP=FN=1, accuracy 2/4 and false-accept rate 1/2. Report that
  numerator and denominator. Review the two disagreements and calibrate on
  different human-labeled traces. Correlation undermines a binomial interval.
- **D57.** Answer passes, requested trajectory differs, and actual write count
  remains zero if the handler was never entered. A strict whole-case outcome
  fails. Keep requested, attempted, and completed operations separate.
- **D58.** This fixture establishes that one scripted request reached the
  policy boundary and produced no unauthorized effect. It does not estimate
  attack success against a live model. Move the same note from evidence to a
  different input origin and verify the policy still verifies origin.
- **D59.** Valid arguments cannot authorize an absent allowlist grant.
  Assert the denial category and a zero handler call counter. Inject a
  failed admission or stale revision before dispatch and test that no
  persistent effect occurs.
- **D60.** Export the reviewed event, status and duration fields. Duration
  and percentiles use seconds. IDs can correlate sensitive actions and raw
  arguments can contain secrets. Compare paired inputs across routes and
  report cost per success only when accounting is complete.

## Week 11

- **D61.** Query by job ID and authenticated owner. A different valid bearer
  identity gets 404 and no input, result, owner, or job fields. Session ID
  from a request is a name, and requires the server's independent ownership
  condition in every query.
- **D62.** Capacity is 3/8=0.375 jobs/s and utilization is 0.5/0.375≈1.33.
  The ideal queue already saturates. Return the original job for a repeated
  matching key, and conflict if payload differs. Test cancellation before
  dispatch, worker cancellation while executing, and a simulated commit
  before cancellation separately.
- **D63.** Claim in a short write transaction conditional on eligible queued
  or expired work. Reject completion unless lease token and running state
  match. Resolve an uncertain remote effect by asking the remote status with
  the matching operation ID, or hold it unknown for operator reconciliation.
- **D64.** Emit safe status transition logs, count completed requests, record
  execution seconds in mergeable distributions, and time the run in a span.
  For job timestamps, queue time is start−accepted, execution is
  finish−start. Instance-level percentiles only preserve ranks inside those
  samples. In-memory export checks span schema and lifecycle, not deployment
  exporter connectivity or access policy.
- **D65.** Capacity is 0.4 jobs/s and utilization 0.75. Four requests fit now
  and the next token arrives after 20 seconds. Estimated cost is
  $0.001 input + $0.001 output = $0.002. Unknown usage remains unknown;
  discounts, cache charges or retry billing can change the invoice.
- **D66.** The process writes /data/jobs.sqlite3 to a mounted named volume.
  Process restart preserves the mounted data, host loss needs a restored
  backup. Three independent 30/minute buckets permit about 90/minute.
  Mount a readable credential file with constrained permissions and check
  readiness separately from liveness. Force lease expiry and confirm the
  new token fences the original completion.

## Week 12

- **D67.** Enumerate bounded paths, sort ties by relative path, validate the
  closed schema before dispatch, and reject invalid paths through the
  owned-workspace guard. Decode explicit UTF-8 under the byte cap. Editing
  bytes changes the revision under normal collision-resistance assumptions.
  Lexical occurrences do not establish call relationships. Seed a unique
  token after the file cap and inspect whether coverage was declared.
- **D68.** Expected evidence order is observation, proposal, approval, apply,
  and applicable test at the applied revision. Missing predecessors invalidate
  a trajectory. Persist a typed pending decision before dispatch. Reconcile
  apply by intent and current hashes. Preserve the unknown enum when migrating.
  A correct-looking final message or a mandatory test on a pure read can
  both cause invalid grading outcomes.
- **D69.** Verify proposal identity, session, tool, canonical arguments, path,
  base and replacement digests. The distinct hashes bind the before and after
  text. Re-read under policy at apply; after a crash, compare current bytes with
  both expected revisions. Authenticated receipts require reviewer identity,
  decision timestamp, expiry and binding; an ordinary caller method has no
  built-in identity assurance. Approval does not prove program semantics.
- **D70.** Host chooses argv and authorized root; backend enforces timeout,
  mounts, network and environment. Cancellation can prevent dispatch or
  abandon a local wait; it cannot undo a completed process action. Reconcile
  with backend operation status and a revision identity. A fake backend
  checks adapter calls only. Use the namespace smoke to check actual
  boundaries on the supported host.
- **D71.** Restore full event 8 if it supersedes checkpoint 7. An after hash
  supports reconciliation as applied; a before hash requires renewed review
  before retry; other state is unknown. Restored approval is cleared.
  Checkpoint identity binds task, provider class, model, budgets and tools.
  Persist pending calls, observations, request messages, counters and deadline.
  A token estimate guides selection; provider usage supports accounting.
- **D72.** Report 8/10 functional passes and 3/3 refusals separately. Hard
  authorization failures block passing even with a high aggregate.
  Correlated visible fixtures are limited coverage, not independent samples.
  Freeze split and grading before evaluation. If results affect tuning,
  retire that split as a final estimate and draw a new held-out set.
  Demonstrate an actual timeline and tie result evidence to exact bytes.
