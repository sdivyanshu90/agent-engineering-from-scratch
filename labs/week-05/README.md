# Week 5 independent labs — reliable model application boundary

Prerequisite: finish Phase 2. Copy runnable baselines into `learner-work/week-05/`.
They execute but intentionally fail the full contract. Attempt independently,
then use [hints](hints.md) and [separate references](../../solutions/labs/week-05/explanation.md).
Ordinary checks require no API key, network, GPU or paid model.

| Day | Starter | Contract |
|---|---|---|
| 1 / D25 | [adapter.py](starter/adapter.py) | request_payload(Request) preserves model/messages/max_output_tokens/store=False. decode_response accepts only completed text-only assistant envelopes (reasoning items may be skipped), validates usage/ID, rejects refusal, unknown output and incomplete status with ProviderError. |
| 2 / D26 | [prompts.py](starter/prompts.py) | prompt(source,model,version='v1') builds known-version bounded role-separated Request; fingerprint(request) hashes canonical UTF-8 request with SHA-256, preserving message order and all fields. |
| 3 / D27 | [output.py](starter/output.py) | validate_output(text) returns Classification with exact category/summary/urgent fields, strict types/enum, nonblank summary≤120 code points, body≤4096 UTF-8 bytes, duplicate/extra rejection. |
| 4 / D28 | [stream.py](starter/stream.py) | async collect(events,max_bytes=4096) accepts exact delta/done dictionaries; bounds aggregate UTF-8 bytes, requires done then exhaustion, rejects later events/truncation/errors, closes async generators and propagates cancellation. |
| 5 / D29 | [recovery.py](starter/recovery.py) | async call(provider,request,attempts=3,deadline=2,base_delay=.01,sleep=...) retries only ProviderError.retryable, one overall deadline, attempts1..10, base_delay0..1, no trailing sleep, cancellation/permanent failures propagate. |
| 6 / D30 | [accounting.py](starter/accounting.py) | estimate(Usage,input_rate,output_rate) returns Decimal using per-million units; finite nonnegative numeric rates, invalid rates reject. Usage already validates genuine nonnegative integer counts. |

Run `python labs/week-05/checks.py --day 1` for the reference. Add
`--module learner-work/week-05/adapter.py` to select your own file; change day/file
for other contracts. Run `python scripts/validate_exercises.py` for every authored
reference. Public checks are the minimum; submit two original boundary tests,
a hand trace, a reproduced/fixed defect and the day's examination.

The optional comparison uses `uv sync --locked --extra schemas` with pinned
Pydantic. It does not replace the required first-principles parser and has a
distinct raw duplicate-key parser policy. Demonstrate the full fake-provider
classification path and a report retaining invalid/wrong-label/unknown-usage
outcomes. Do not label supplied fixture results as real-model quality.
