# Week 2 daily and weekly reference criteria

Attempt first. Daily items earn one point each only with a concrete correct
answer; at least four including independent code are required.

## D07
1. IP locates destination, port locates endpoint, TCP carries ordered bytes,
   HTTP frames method/path/headers/body, JSON encodes a body value. Explain layers.
2. Byte length must be calculated after exact UTF-8 serialization; non-ASCII
   code points may occupy multiple bytes.
3. Use [validator](../../forgeagent/api.py); an independent attempt must reproduce
   the contract including duplicates/types/bounds, not import it.
4. Parsing success alone cannot establish exact keys or field types; duplicate
   hooks reject ambiguity rather than silently accepting a later value.
5. A body owner field is attacker-controlled. Derive owner from authenticated
   state and constrain every resource access by that owner.

## D08
1. Table has named columns and rows; key identifies unique records; connection
   is a resource; transaction is an atomic state-change boundary.
2. Same identifier under alice/bob creates separate composite keys.
3. Explicit commits, rollback experiment, per-call connection close, parameters.
4. `if not text` treats empty as missing; `text is None` preserves distinction.
5. Short connections simplify worker ownership but add overhead; long shared
   connections require thread and transaction coordination.

## D09
1. Processes separate address spaces; threads share one; coroutine is suspended
   async work; task schedules it; loop coordinates ready work/I/O.
2. Both tasks can yield at await before either completes; input-order output
   is established by result collection order, not scheduler luck.
3. TaskGroup owns children, completion and sibling cancellation; inspect results
   after scope exit. See [collector](../labs/week-02/concurrent.py).
4. Blocking sleep holds loop thread; use async sleep or appropriate thread offload.
5. Concurrent independent reads, then await/validate both before a dependent write.

## D10
1. Timeout limits waiting; deadline limits a larger operation by absolute time;
   cancellation requests stopping; transient classification authorizes a retry
   only under an operation-specific repeatability policy.
2. Four attempts have sleeps .1,.2,.4, total .7 seconds.
3. See [retry](../../forgeagent/async_ops.py); no trailing sleep and no cancellation retry.
4. Catching BaseException can swallow CancelledError; synchronize start, cancel,
   await propagation, and verify cleanup with an event.
5. Reconcile stored state or use an idempotent request key; no acknowledgment
   does not establish no effect. A thread may commit after timeout.

## D11
1. Vector is ordered coordinates; norm length; matrix shape rows×columns;
   event subset of outcomes; conditional probability rescales within an event.
2. Dot([1,0],[1,1])=1; norms 1 and √2; cosine=1/√2≈.7071.
   Choose your own rectangular product and show matching inner dimensions.
3. Shape checks before zip; zero norm rejected. Reference in math_basics.py.
4. Zip truncation masks mismatched dimensions; zero direction is undefined.
5. Cubing failure assumes independent per-attempt causes. Shared schema defects
   survive retries; compare conditional groups rather than hiding correlation.

## D12
1. Derivative local rate, partial changes one variable, gradient collects partials;
   log inverts exponent on positive domain. Demonstrate with a number.
2. Derivative 6(3x+1), at 2 is 42. Square descent from 2 at .1 gives 1.6 then 1.28.
3. Shift max before exp; finite differences compare with an independently derived rate.
4. Overflow is a numerical-form problem; missing inner derivative loses factor 3.
5. Finite differences require repeated function evaluations per coordinate and
   face cancellation/step-size error; useful checker, costly training mechanism.

## Weekly conceptual and architecture criteria

Award the fixed 2+1+1 conceptual points for correct distinctions, causal mechanism,
and concrete limitation. A high-level slogan is not four points. Coding uses
[the six contracts](../../labs/week-02/README.md) and actual execution evidence.
Debugging requires the first wrong state, not just the eventual exception.

Math answers: dot=20, norms=5 and 5, cosine=.8; composite derivative=42 at x=2;
softmax [0,ln2] gives [1/3,2/3]. Translation multiplies numerator/denominator by
same positive factor, canceling. Four-attempt delay sum .7. Shared permanent
failure invalidates the independence model behind 1−.2³=.992.

Integration: same owner roundtrip 200; other-owner GET 404; reopening retains
text; malformed input 400 with no write; injected storage OperationalError 503
without exposing internal details. Authentication absent is 401, independently
of whether the body is valid. Execute each case; do not grade predicted outputs
as observed results. No score overrides the weekly critical criteria.
