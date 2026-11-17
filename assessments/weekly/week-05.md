# Week 5 mastery examination

Attempt independently before [answers](../../solutions/examinations/week-05.md).
Suggested one focused day, standard-library docs allowed. No paid call required.

Conceptual, 20 points: distinguish five pairs (four points each: correct claim 2,
mechanism 1, example/limitation 1): SDK completion/task success; role/content;
schema/semantics; stream delta/final value; allowance/actual usage.

Coding, 30 points: six [lab contracts](../../labs/week-05/README.md), five each
(normal result 2, boundaries 1, independent explanation/tests 2). Implement the
mechanism, not a wrapper importing the reference. Optional Pydantic comparison
must explain raw duplicate-key policy rather than assume identical parsing.

Debugging, 20 points: four failures, five each (minimal reproduction 1, first
wrong state 2, fix/regression 2): incomplete response accepted as text; source
promoted into developer instructions; truncated stream returned as success;
cancellation treated as retryable. Preserve actual observed outputs/errors.

Architecture/math, 20 points: four defenses, five each. Draw all validation
boundaries; derive three-attempt backoff and one overall deadline; explain two
independent local gates violating shared limits; calculate hypothetical
I=1000,O=200,a=2,b=8 per-million cost and distinguish unknown failed usage.

Integration, 10 points: fake-provider complete classification path (3), malformed
output failure (2), wrong-label semantic failure despite schema validity (2),
all-attempt quality/cost report with prompt/model identity (3). These are contract
checks; do not present supplied fake answers as real-model predictive performance.

Pass at 80/100 plus critical invariants: no role promotion, no partial-success
stream, cancellation propagates, finite attempts/deadline, valid units and no
fabricated live results. Remediate and repeat changed fixtures without changing
grading criteria after observing outcomes.
