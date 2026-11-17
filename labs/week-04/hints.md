# Graduated hints

| Day | Conceptual | Algorithmic | Implementation |
|---|---|---|---|
| 1 | A merged symbol consumes both operands | Scan once per ranked pair | Advance by two on match, one otherwise; allocate fresh output |
| 2 | IDs are not vectors | Add content/position, then three weighted-row maps | Validate row width before zip; q/k output widths must match |
| 3 | Eligibility precedes probability mass | Dot, divide by sqrt(width), softmax, mix values | Shift max; keep key/value ordering aligned |
| 4 | Constant coordinates must be defined | Mean, mean squared deviation, sqrt(var+epsilon) | Use population denominator n, not n−1 |
| 5 | Avoid logging a rounded-zero probability | logsumexp minus target score | Subtract common maximum before exp |
| 6 | Filter ordering is part of the model contract | Temperature, top-k, normalize, nucleus prefix, sample | Greedy is a separate T=0 branch; seed a local Random |
