# Week 5 reference criteria

Daily questions award one point each for concept, trace, independent code,
debugging and judgment; require four including code. Weekly rubric is fixed
at 20/30/20/20/10, with all critical invariants mandatory.

D25: request → wire → transport → completed envelope → application validation.
Refusal/incomplete/unknown tool output must reject in the text-only adapter.
Usage must be genuine nonnegative integers. Mock success is not live compatibility.
An SDK may replace translation while retaining the application-owned contract.

D26: trusted developer template remains separate from user source. Preserve
ordered messages and all model/settings/version fields in canonical UTF-8 SHA-256.
Digest length is 64 hexadecimal characters. A hash neither anonymizes low-entropy
text nor authorizes another owner to read a response cache. Unknown version rejects.

D27: parse syntax, validate shape, check business rules, evaluate support separately.
Strict urgent rejects 1/'false'; nonblank summary rejects spaces. Duplicate keys
must reject before a raw parser silently selects one. Pydantic strict models
validate at invocation, unlike ordinary hints; their JSON parser policy can differ.
A valid but factually wrong label still needs separate semantic grading.

D28: collect deltas under aggregate UTF-8 byte bound, require done then exhaustion,
reject later events and truncation, close on every path. Two é characters use
four UTF-8 bytes. Cancellation propagates; local close does not establish remote
billing stopped. The implementation is a normalized stream protocol, not a tested
live SSE bridge. Provisional UI text cannot authorize partial tool arguments.

D29: all attempts/backoff share one timeout. Retry only classified eligible failures;
no trailing sleep. Three attempts at base .1 sleep .1+.2=.3. Two local gates can
exceed a shared quota. Fallback must satisfy capabilities/data/quality constraints;
no automatic routing equivalence is claimed. Unknown transport outcome is not
proof of no remote work or charge.

D30: hypothetical cost=(1000×2+200×8)/1e6=.0036. Decimal avoids avoidable display
arithmetic errors; rates require explicit units. Total cost over all attempts
is divided by successful tasks. Unknown failed usage is not zero. Invalid
outputs remain in the fixed denominator; fake-provider success measures software
contracts only. A report omitting these distinctions fails even with green code.

For weekly debugging, require a minimal local fixture and first incorrect state,
not a generic recommendation to “improve the prompt.” Use the published point
allocation; no correctness point from a copied reference or invented observation.
