# Week 10 — evaluate and secure agent systems

Week 10 turns bounded agents into something measurable and reviewable. Day 55
freezes ground truth and deterministic grading; Day 56 calibrates supplied
model-grader scores and discusses repeated trials; Day 57 grades task success,
tool choice, and full trajectories; Day 58 places prompt injection in poisoned
observations; Day 59 enforces least privilege and injects runtime faults; Day 60
uses safe telemetry for quality/latency/cost decisions. No live model or paid
service is required. The benchmark evaluates the actual `Agent` class using
fixed provider decisions and tool handlers.

The public development split is for iteration. The fixed heldout fixture is
deliberately separate and requires an explicit final-evaluation flag. The fixture
source is visible; it is not a secret test set. Do not tune against its cases.
See the [frozen protocol manifest](../../docs/week-10-manifest.json),
[labs](../../labs/week-10/README.md), [weekly exam](../../assessments/weekly/week-10.md),
and [Phase 5 exam](../../assessments/phase-examinations/phase-05.md).

## Source record

- OWASP GenAI Security Project, “LLM01:2025 Prompt Injection,” accessed
  2026-11-17: https://genai.owasp.org/llmrisk/llm01-prompt-injection/. The page
  distinguishes direct from external-source indirect injection and recommends
  least privilege and adversarial testing. This informs threat design; it does
  not certify the local runtime.
- OpenTelemetry, “Semantic Conventions,” accessed 2026-11-17:
  https://opentelemetry.io/docs/concepts/semantic-conventions/. It describes
  common names for telemetry operations and data across traces, metrics, logs,
  profiles, and resources. The local summary is not an OTel exporter.
- OWASP Cheat Sheet Series, “LLM Prompt Injection Prevention,” accessed
  2026-11-17: https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html.
  It states string screening is not a security boundary and advises testing the
  external content channel for indirect injection. This directly motivates the
  boundary-oriented fixture design.
