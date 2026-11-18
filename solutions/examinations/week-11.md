# Week 11 examination — answer reasoning

## 1. Identity boundary

The trusted token maps to `owner-A`; body field `owner-B` is untrusted data and
does not alter identity. The lookup must be equivalent to
`WHERE job_id = ? AND owner = ?`, with values `j-3` and `owner-A`. A foreign or
absent row receives the same not-found response. A session ID and random job ID
are names, not credentials. A JSON owner field is likewise not authority.

## 2. Async admission

Long work can outlive a client connection or reverse-proxy timeout. The route
validates and durably admits a job, returning 202 to say processing was accepted;
it does not say the run succeeded. The status resource reports the current
owner-scoped state and safe result/error code. An unbounded queue converts
overload into growing memory or disk use and increasingly long waits.

## 3. Idempotency

The matching owner/session/key and same body resolves to the existing job ID,
without another insert. The same key bound to changed input is a conflict because
otherwise retries could silently change the meaning of one operation. This
deduplicates job admission only. It cannot make a remote tool side effect happen
exactly once if a worker crashes after the effect and before recording success.

## 4. Capacity

Ideal capacity is `c/S = 4/10 = 0.4` jobs/second. Utilization is
`ρ = λ/(c/S) = 0.3/0.4 = 0.75`. With end-to-end average `W=18` seconds,
`L=λW=0.3*18=5.4` jobs in system on average. High service-time variance, bursts,
queueing, or downstream provider limits can make p95 high even below the average
capacity estimate.

## 5. Cancellation

The API transaction sets `cancel_requested` on the running job. A local process
may cancel the active handler directly; a remote worker polls the persisted flag
during lease heartbeats and cancels its handler. Cancellation is cooperative and
only stops work that honors it. A remote request or filesystem write can already
have completed; a cancellation state cannot roll that effect back. Inspect its
operation receipt and reconcile uncertain outcomes.

## 6. Lease fencing

Completion must update only when the row remains `running` and its current
`lease_token` equals worker A's token. Worker B replaces the token on reclaim,
so A affects zero rows. Renewal keeps the claim alive but does not atomically
combine a database commit with a remote tool operation. Exactly-once external
effects need an idempotent downstream API or a durable intent plus reconciliation.

## 7. Telemetry privacy

A safe event can be `{event: "job_finished", state: "failed", code:
"handler_failed"}` if the code is in the approved finite set. A metric can be a
failure counter labeled by finite state and error code. A span may be named
`agent.job` with state and step count. Exclude prompt text, bearer token, owner,
session/job ID, tool arguments, and raw exception. In-memory export proves the
local SDK recorded a finished span with expected attributes. It does not prove
network delivery, collector security, sampling, retention, or dashboards.

## 8. Cost and rate limits

From full capacity, three requests can consume the immediate burst. One token
refills every 30 seconds. Estimated input cost is `2,000 * $0.50 / 1,000,000 =
$0.001`; output cost is `500 * $2 / 1,000,000 = $0.001`; total is `$0.002`.
Missing usage must stay unknown, not be encoded as zero. Provider billing can
include retries, caching, or pricing terms absent from the estimate.

## 9. Persistence and Week 8

The job row tracks ownership, state, attempts, and lease. A session event records
ordered domain progress under an owner/session revision. An operation receipt
records intent and outcome for one external side effect. If the remote effect
timed out after it may have succeeded, mark the operation `unknown` (or leave a
pending intent subject to explicit reconciliation) and inspect downstream state
before retry. Do not infer failure from a missing response.

## 10. Deployment/recovery

The sample image runs as a nonroot user, receives the bearer token at runtime
from an approved secret source, and mounts a persistent `/data` SQLite file. It
is a single-host reference; each independent local SQLite database has its own
queue and cannot provide shared claims, status, or cancellation. A recovery drill
submits a fake job, waits until running, stops the service abruptly while keeping
the volume, restarts against the same file, waits for lease expiry, checks attempt
count increments and completion, and verifies a stale token cannot overwrite the
new result. Check Week 8 receipts before replaying an external effect.

## Scoring and remediation

Award points for correct invariants and reasoning, not exact wording. Any answer
that trusts a request body owner, states cancellation reverses an external
effect, or claims exactly-once behavior from a lease caps the exam at 79 until
that misconception is corrected. Reattempt with a new owner/job/token and show
the modified SQL or transition predicate.
