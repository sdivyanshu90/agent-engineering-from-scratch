# Graduated hints

Use the smallest hint needed, then attempt independently.

| Day | Conceptual | Algorithmic | Implementation |
|---|---|---|---|
| 1 | Shape and syntax are different checks | Decode, parse, compare exact fields/types | json.loads hooks expose duplicate pairs and non-finite constants |
| 2 | A document belongs to an owner/id pair | Query with both components, transaction around writes | Use ? parameters, autocommit=False, connection context plus explicit close |
| 3 | Scheduling order need not determine result order | Create all tasks, wait for ownership scope, read in input order | TaskGroup and task.result after scope exit |
| 4 | Retry only a classified, repeatable failure | Loop finite attempts, timeout each, sleep only before another | Catch TransientError alone; inject sleep to observe delays |
| 5 | Shapes are part of the contract | Sum coordinate products and normalize by both lengths | Validate before zip; norm is sqrt(dot(x,x)) |
| 6 | Equivalent algebra can avoid overflow | Subtract a common maximum before exponentiation | Use exp(z-max), divide by summed weights; square gradient is 2x |
