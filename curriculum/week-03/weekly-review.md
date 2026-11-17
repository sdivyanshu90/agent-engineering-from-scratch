# Week 3 review and remediation

Closed book, reconstruct partition invariants and trace one regression update.
Draw a nonsquare two-layer forward pass and count parameters. Rebuild addition,
multiplication, and reverse propagation from their contracts, then demonstrate
shared x*x and shared intermediate a+a. Train a finite XOR loop and identify
precisely what that demonstration measures. Derive a smoothed bigram row and
held-out mean NLL without running code first.

Take [the exam](../../assessments/weekly/week-03.md) before consulting references.
Remediate by observed failure: data overlap → freeze/group splits; wrong update
→ coordinate gradient check; shape bug → nonsquare fixture; missing gradient
→ shared-path trace; stale graph → rebuild after updates; misleading LM score
→ fix vocabulary, boundaries and n−1 denominator. Repeat with changed inputs.

One week later reconstruct two unrelated mechanisms, one numerical and one
state/ownership contract. Record failed predictions and correction evidence,
not just final green checks. No score converts the fitted XOR truth table into
a held-out generalization claim.
