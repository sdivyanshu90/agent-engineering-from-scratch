# Week 2 reference reasoning

The API, storage, recovery, and math references are shared with the evolving
ForgeAgent components; solution modules re-export those implementations rather
than maintain an inconsistent copy. Read the actual linked source after an
independent attempt. The concurrent collector is implemented directly here.

1. [Validation](../../../forgeagent/api.py): byte bound → strict decoding → parse
   with duplicate/non-finite rejection → exact key/type contract → text-length
   bound. This is structural validity, not factual correctness or authorization.
2. [Storage](../../../forgeagent/storage.py): composite primary key enforces
   owner/id uniqueness, parameters keep values out of SQL structure, and short
   explicit transactions commit or roll back. Closing is separate from commit.
3. [Concurrent collector](concurrent.py): create all tasks before waiting; group
   exit owns completion/cancellation. Reading results in original task order
   separates output order from scheduling order. A failure raises rather than
   misrepresenting partial success as a complete list.
4. [Recovery](../../../forgeagent/async_ops.py): exactly one operation per attempt;
   only TransientError reaches the backoff path. No sleep after final failure.
   Timeout/cancellation are intentionally not relabeled as retryable. Threaded
   work may continue, so recovery must reconcile uncertain effects.
5. [Vectors](../../../forgeagent/math_basics.py): explicit shape checks prevent
   zip truncation; cosine checks zero norm. Moderate finite inputs are the stated
   contract; extreme floating-point overflow needs additional numerical design.
6. [Optimization](../../../forgeagent/math_basics.py): central differences check
   derivatives; the square update uses analytic gradient 2x. Stable softmax shifts
   by the largest score, retaining an equivalent ratio with no positive exponent.
   Extremely negative shifted weights may underflow; later log-probability code
   needs log-sum-exp rather than taking logs of rounded zeros.

A correct solution includes the explanation and independent boundary tests.
Importing the reference into a learner submission demonstrates reuse, not the
independent implementation competency being assessed.
