# Week 4 review and remediation

Closed book, reconstruct representation flow from text to IDs to vectors to
logits to sampled IDs. Trace a nonoverlapping merge and a position projection.
Derive a two-key attention output, draw a three-position causal dependency table,
and compute normalization of [1,3]. Count the toy decoder's parameters and derive
cross-entropy logit gradients. Explain shifted labels versus teacher-forced inputs.

Run full/cached logits on three prefixes, then intentionally use a stale cache
after a parameter edit and reproduce disagreement. Restore/clear state rather
than relaxing tolerance to hide the defect. Trace nucleus filtering by hand.
Take [the weekly exam](../../assessments/weekly/week-04.md), then
[Phase 2 cumulative exam](../../assessments/phase-examinations/phase-02.md).

Remediate by cause: lost source characters → nonoverlap/roundtrip; wrong vector
→ shape/ID compatibility; future leakage → eligibility and normalization axes;
NaN → finite domains and stable algebra; wrong training objective → shifted
labels; cache mismatch → position/prefix/model revision; endless generation →
explicit finite step/context bounds. Retest new fixtures after remediation.

One week later reconstruct one math mechanism and one ownership invariant.
A plausible sample is not a metric, a low toy loss is not useful coding ability,
and a correct transformer does not implement an agent harness.
