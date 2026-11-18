# Final examination reference rubric

The final defense is graded on the system's actual artifacts, not projected
capabilities. A high-quality presentation identifies trust boundaries and
provides one trace for observation, proposal, human authorization, apply, and
verification. It includes at least one boundary rejection and an accurate
description of what each check establishes.

The recovery demonstration must use a new agent/session object, preserve the
pending decision and budget counters, and avoid duplicate provider decisions or
writes. Proposal receipts are validated and become unapproved after restart.
Ambiguous operations are reconciled or left unknown; they are not silently
replayed.

The evaluation report preserves all fixed cases and clear denominators. It
labels development and held-out data, notes any leakage or post-inspection
tuning, and separates protocol integration from autonomous coding quality.
Known limitations include path check race assumptions, the fact that an
injected backend is not automatically isolated, lossy context, provider
variability, and limited visible fixtures.

Pass requires at least 80/100 and no critical boundary violation. A missing
production result is not a penalty if reported honestly; fabricated or
overclaimed evidence is a critical failure. The learner must describe one
bounded follow-up experiment and its expected measurable result.
