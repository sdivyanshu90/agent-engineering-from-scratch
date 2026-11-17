# Week 6 mastery examination

Attempt before [answers](../../solutions/examinations/week-06.md). Suggested
one focused day; no external models/services required.

Concepts, 20 points: five distinctions, four each (claim2/mechanism1/limitation1):
source/chunk revision; tf/df; representation/index error; fusion/reranking;
citation occurrence/truth/authorization. Use concrete counterexamples.

Coding, 30 points: six [lab contracts](../../labs/week-06/README.md), five each
(normal2/boundary1/independent reasoning2). A copied engine or reference import
cannot replace implementing the assessed mechanism. Preserve IDs and exact policies.

Debugging, 20 points: four failures, five each (reproduce1/cause2/fix-regress2):
zero-stride overlap; silent vector truncation; duplicated rank entries inflating
scores; stale or real-but-unselected citation accepted. Record actual evidence.

Math/design, 20 points: derive BM25 equal-length fixture; cosine sign-bucket miss;
RRF [x,y]/[y,z]; graded nDCG [b,x,a] with a:2,b:1. Five points each for complete
symbols/conventions/arithmetic and interpretation. Precision uses fixed k.

Integration, 10 points: run fixed corpus benchmark preserving all rows (3),
explain visible versus held-out scope (2), demonstrate quote-only model path with
FakeProvider (3), identify real-source false-relevance limitation (2).

Pass80/100 plus critical invariants: authorized evidence before prompt, stable
revision association, no duplicate inflation, no unsupported extra answer claims,
explicit no-evidence abstention and no fabricated semantic/live benchmark results.
Correct failures, then retest new data without changing grading after outcomes.
