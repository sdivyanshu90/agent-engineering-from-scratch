# Week 10 laboratory notes

These six contracts isolate common evaluation mistakes. A route report must
compare the same cases and count failures in its denominator. Wilson uncertainty
is large at small n: four successes in four trials still does not imply certainty.
Redaction uses omission and a field allowlist, so newly added payload keys are
excluded unless explicitly reviewed. Hashing raw bytes catches even formatting
changes because the benchmark freeze includes the exact source artifact.

Calibration uses supplied human labels, not a live model call. Its agreement
rate measures matching labels only; it does not establish that the humans were
right or representative. Boundary checks inspect actual execution effects and
status. They intentionally do not count whether the phrase “ignore policy” was
present in task text: security behavior is an observed authorization invariant,
while prompt-injection robustness requires repeated model-mediated trials.
