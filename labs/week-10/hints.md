# Hints

1. Normalize by case count only after counting pass/fail; keep time in seconds.
2. Wald intervals are poor near 0 and 1; use the Wilson center and half-width.
3. Define an allowlist first. Redact by omission, not replacement after logging.
4. Hash raw bytes, not decoded/re-serialized JSON.
5. Treat human labels as a finite calibration sample and report disagreement.
6. Assert that an effect did not happen when permission is absent. A prompt string
   alone cannot prove that an adversary was contained.
