# Week 8 examination — reference answers and reasoning

## A. Workflow planning and evaluation

Layers: `{inspect}`, `{patch,test}`, `{verify}`. Alphabetical tie-breaking may
place `patch` before `test`. Validate the complete identifier set and all edge
references before computing any ready layer; a missing parent or cycle raises
before the fake executor is invoked. Fixed criteria bind to candidate digest and
rubric version. Any edit changes the digest, invalidating earlier results.

## B. Context, provenance and memory

First apply authorization; exclude any README outside the allowed source set.
Under the local ordering, fresh candidates sort by lexical overlap, then trust,
recency and ID. Charge the reserved policy item first. At budget 20, whether the
policy estimate is 7 and test result 9 both fit; a README estimate of 10 would
not fit after those two (26), so test is selected. Stale memory is dropped before
scoring. Tool output remains tool-origin untrusted evidence; it cannot be
retyped as developer policy. Byte/4 differs by tokenizer and language. For a
source-bound fact, require stored revision to match the current source revision,
even if TTL has not elapsed.

## C. Lossy compaction

Prefix truncation may retain “unit tests passed” and omit “integration tests
skipped.” A structured handoff should retain claim, caveat, source ID/revision,
created time, expiry and a derived/untrusted authority label. Whole-item exclusion
preserves each selected item's text; compaction deletes text inside retained
items and must mark loss explicitly.

## D. Event journal and checkpoint

One writer appends revision 9 under a transaction that compares current=8,
updates session revision and inserts event. The second writer also expecting 8
observes current=9 and conflicts. Resume loads state snapshot at revision 9 and
ordered events 10 and 11. Scope every query and key by owner/session; bound finite
JSON and validate schema version. SQLite cannot atomically commit a remote tool
effect, email, payment or shell process.

## E. Resume, idempotency and recovery

Crash before call leaves pending but likely no effect; confirm before dispatch.
Crash after remote commit but before receipt leaves pending and unknown reality;
query provider status by same key or request reconciliation, never infer failure
from timeout. After receipt, replay returns immutable same result. Canonicalize
finite JSON and bind operation ID to SHA-256 digest; same ID/digest is replay,
changed digest conflicts. Without remote status or dedupe, surface unknown for
owner/operator reconciliation; retry policy cannot prove no duplicate.

Passing requires correct boundaries, not claims that this fixture provides
distributed transactions or exact remote execution counts.
