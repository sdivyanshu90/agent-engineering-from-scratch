# Hints in increasing detail

| Day | Conceptual | Algorithmic | Implementation |
|---|---|---|---|
| 1 | Randomness and partition roles are separate | Copy, seeded shuffle, two boundaries | Check IDs before slicing; fixed ordering is part of reproducibility |
| 2 | Both derivatives use old parameters | Build residuals once, average r*x and r | Multiply both means by two before subtracting scaled gradients |
| 3 | Shape determines matrix orientation | Weighted rows plus bias, ReLU, next layer | Reject inconsistent row lengths before zip can truncate |
| 4 | Shared paths add influence | Record parents/pullback, topological visit, reverse | Reset, seed root one, use += for each operand role |
| 5 | Gradients describe the old forward computation | Finish backward before any data update | Validate rate and parameter identities first; then update each leaf once |
| 6 | Unseen events still need mass | Initialize every pair, count, normalize selected row | Denominator includes smoothing for the entire vocabulary |
