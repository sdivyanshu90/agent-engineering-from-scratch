# Week 8 review — plan, context, persist, reconcile

Close the code and reconstruct the following from memory, then check against the
references only after the attempt.

1. Draw a five-node DAG with a fork and join. Compute stable layers. Add a cycle
   and say where validation rejects before any effect.
2. Explain why a second model evaluator is not independent evidence by default.
   Write a fixed criterion and one observable evidence pointer.
3. Given context items with role, trust, revision, creation time and TTL, identify
   which are eligible, which are authorized and which fit the heuristic budget.
   State where an authorization filter belongs.
4. Compact a finding and state exactly which source IDs/revisions survive. Name
   one qualification that might be lost and how a critical decision re-fetches it.
5. Trace two writers using the same SQLite expected revision. Identify the
   transaction that commits revision and event as one unit.
6. Draw the intent/effect/receipt crash timeline. For pending state, give both
   possible realities and one safe recovery action for each.

Retrieval schedule: after one day repeat the DAG and CAS traces; after three days
redraw the uncertain-effect timeline; after one week reproduce a stale-memory
case. Mark mastery only after code checks and a written explanation both pass.
