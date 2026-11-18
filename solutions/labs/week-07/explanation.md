# Week 7 lab reference notes

Day 1 sends fixed-format tasks to an authored parser route, ambiguous requests
to a decision loop, and low-confidence cases to review. Confidence is a routing
input, not proof that the resulting answer is correct.

Day 2 checks a deliberately small closed schema language. `type(value) is int`
is required because Python considers booleans integers for `isinstance`; string
limits count UTF-8 bytes. Tool schemas constrain input shape, while the caller
allowlist and handler environment control authority.

Day 3 preflights every call in one decision before invoking the first handler.
This prevents a later unknown tool from causing partial effects. Expected
handler `TypeError`/`ValueError` become observations; malformed protocol fails.
The reference is intentionally smaller than ForgeAgent's production loop.

Day 4's repeated scan is simple, stable and quadratic in the worst case. Real
runtime batches are capped at eight, making clarity a reasonable trade. Returned
layers preserve original order among simultaneously ready nodes. A failure
propagates to descendants only through explicit dependency edges.

Day 5 charges observed usage after a completed model call. `may_continue` is
false at equality, while ForgeAgent permits processing a decision at exact
equality and prevents the next request. Overshoot is recorded, not refunded.
Neither behavior creates a provider-side spending guarantee.

Day 6 returns counts and stable errors rather than prompt content. Production
systems must add access control, retention and redaction policy. Fake traces
make regression tests deterministic; they do not estimate live reliability.
