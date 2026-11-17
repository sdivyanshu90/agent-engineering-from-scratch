# Week 5 review and remediation

Trace one request from trusted prompt construction through serialization,
completion parsing, strict classification and usage. Draw the separate failure
paths for refusal, incomplete completion, malformed output and valid-but-wrong
label. Rebuild fingerprinting and show why it is not authorization or anonymization.

Reconstruct stream-state assembly, demonstrate truncation and cancellation cleanup,
then trace classified retries within one overall deadline. Use a fake clock to
explain local request spacing versus distributed/token limits. Derive hypothetical
cost and a quality report including invalid outputs and unknown failed usage.

Take [the weekly examination](../../assessments/weekly/week-05.md) before
[reference criteria](../../solutions/examinations/week-05.md). Remediate the first
wrong boundary: role promotion, coercion, missing terminal event, cancellation
retry, unit error or changed denominator. Retest with changed fixtures. No live
model call is needed, and fake-provider results must remain labeled as contract
evidence rather than model-quality measurements.
