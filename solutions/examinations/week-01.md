# Week 1 examination answers and grading guidance

Attempt the daily and weekly questions first. Grade behavior and explanation,
not exact wording. Public lab checks are necessary but not sufficient.

## Daily criteria — one point per item

### Day 1
1. File is saved source; process is a running interpreter; stdout is an effect,
   not saved program state. Distinguish all three.
2. Final x=10, y=5. y was computed once from the earlier x=2.
3. Independent summary uses string length and whitespace-split length, including
   correct empty input. See [reference](../labs/week-01/summary.py).
4. `"a  b"` has two words but two spaces; spaces+1 gives three. Empty text gives
   one by that rule but zero by contract.
5. State a precise punctuation policy and an example it distinguishes. No
   universal linguistic answer is required.

### Day 2
1. `=` binds, `==` compares; demonstrate a result rather than restating symbols.
2. `A,a!` → `a,a` and append; `...` → empty and discard; `?` → empty and discard.
   Final `['a,a']` under the specified edge-strip policy.
3. Independent exact policy, fresh list, no unwanted punctuation removal.
4. Append mutates and returns None; assigning its return replaces the list name.
5. Preserve case when distinguishing identifiers is necessary; compare with
   broader recall from caseless prose search. Defend with a concrete example.

### Day 3
1. Return passes a result to a caller; print writes to an output stream and
   returns None. A caller adding 1 needs the returned count, not a printed line.
2. a is a fresh empty list, b points to the old list and becomes `[2]`.
3. Fresh local dictionary, increment per token, no mutation of input.
4. Default object created at definition time is shared; allocate per call.
5. Set for membership, dictionary for counts, list for ordered events; explain
   how each preserves exactly the required information.

### Day 4
1. Path identifies location; bytes encode data; text is decoded code points.
   `é` is one Python code point and two UTF-8 bytes in its precomposed form.
2. Sorted order is a then b regardless of creation order.
3. Independently read immediate `.txt` files with explicit UTF-8 and error tests.
4. Broad catch erases distinction between complete empty evidence and failed read.
5. Batch gives all-or-failure semantics at corpus-sized memory; streaming lowers
   memory but must define partial-result/error behavior.

### Day 5
1. Hit is a class; `Hit('a',2)` is an instance; path is an attribute; a method
   receives the instance. Give all distinctions.
2. Zero count is filtered. For tied positives compare path after negative count;
   a count 4 precedes 2. Supply concrete keys for your chosen paths.
3. Fresh ranked list, positive filter, explicit limit validation, tie-order tests.
4. Python negative slicing excludes items from the end instead of rejecting the
   request. Validate before slicing; zero is valid and returns empty.
5. Explicit records/functions localize ownership and simplify tests. A shared
   mutable global needs synchronization and lifecycle rules even before a server.

### Day 6
1. Success data on stdout; diagnostics on stderr; status describes process
   success. No match is a valid result, not an operational failure.
2. Count ties break by ascending path; limit 1 retains the first path.
3. Independently compose parse/load/search/serialize and verify no writes.
4. A debug line makes stdout contain multiple formats; remove it or use stderr.
5. Full scan is easy and stateless; repeated queries multiply text work. An
   index can lower query cost but adds ingestion/update/storage consistency.

## Weekly exam reference criteria

A: use the concepts above; award each question's 2+1+1 points only for an
explicit claim, mechanism, and concrete limitation/counterexample.

B: [CLI reference](../../forgeagent/cli.py) and
[document functions](../../forgeagent/documents.py) illustrate a slightly stronger
recursive implementation. Immediate traversal is accepted for the exam if
specified. Score each six-point category proportionally to demonstrated behavior.
Critical errors remain gate failures even if the numerical total reaches 80.
Expected main fixture: `[{"path":"b.txt","count":2},{"path":"a.txt","count":1}]`.
Whitespace differences in JSON formatting are irrelevant; parsed values matter.

C: minimal reproductions:
- Two kept tokens expose append assignment: after first append `result` becomes
  None, then second append fails. Call append without assignment.
- Two distinct tokens expose an early return; empty input also exposes fallthrough.
  Place return after the loop.
- Call a default-dictionary counter twice with one token. Allocate local state;
  regress by mutating an earlier returned value then calling again.
- Feed tied paths in reverse alphabetical order. Add a path secondary key and
  test multiple permutations.
- A missing directory or invalid UTF-8 must raise, then become an explicit CLI
  failure at the appropriate boundary. Do not turn it into an empty success.

D: reward the concrete data path and effect boundaries, an input-sensitive cost
model with assumptions, and explicit acknowledgment of check/open races. No
credit for claiming file-extension filters or frozen dataclasses are sandboxes.

E: valid query and no-match return 0 plus parsed JSON, normally empty stderr;
invalid query, missing directory, and bad encoding return nonzero with no success
JSON and an understandable stderr diagnostic. Each case must be executed, not
merely predicted. Unexpected defects should retain diagnostic detail.

## Diagnostic scoring

Use the corresponding daily criteria. Award 2 only with correct independent
execution/prediction, mechanism, and boundary evidence; 1 for a correct incomplete
explanation, 0 for incorrect/missing. A diagnostic skip requires the same
independence as an ordinary lesson gate. Keep answer inspection after evidence
collection and record assistance honestly.
