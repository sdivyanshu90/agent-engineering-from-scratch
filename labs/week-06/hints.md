# Graduated hints

| Day | Conceptual | Algorithmic | Implementation |
|---|---|---|---|
| 1 | Spans belong to one snapshot | Window with positive stride, stop at final slice | Preserve splitlines keepends; revision hashes full source, ID hashes path/revision/span |
| 2 | tf and df count different things | Build postings/lengths, accumulate one query-term contribution | Positive log1p IDF, saturated tf, length-normalized denominator |
| 3 | Candidate loss is separate from distance | Validate, optionally filter, exact cosine, sort | First-coordinate sign is a deliberate crude approximation, not HNSW |
| 4 | Ranks combine incompatible score systems | Sum reciprocal one-based positions | Reject duplicates within one ranking before counting them twice |
| 5 | Every denominator is a policy | Fixed cutoff, unique hits, first relevant rank, graded DCG/ideal | Exponential gain and empty-ideal zero are explicit conventions |
| 6 | A quote receipt does not prove truth | Parse exact fields, selected snapshot, quote occurrence, full answer | Empty citations permit only explicit abstention; reject extra uncited sentences |
