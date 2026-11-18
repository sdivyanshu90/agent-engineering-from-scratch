"""Manual, local-only OpenTelemetry span example (service extra required).

This demo keeps spans in process memory and prints only reviewed attributes. It
does not configure an OTLP exporter or contact an observability service.
"""
from __future__ import annotations


def capture_demo_span() -> dict:
    """Create and return a small span summary for a fake agent operation."""
    try:
        from opentelemetry import trace
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import SimpleSpanProcessor
        from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter
    except ImportError as error:
        raise RuntimeError("install the optional `service` extra to run the OTel demo") from error

    exporter = InMemorySpanExporter()
    provider = TracerProvider()
    provider.add_span_processor(SimpleSpanProcessor(exporter))
    tracer = provider.get_tracer("forgeagent.demo")
    with tracer.start_as_current_span("agent.job") as span:
        span.set_attribute("job.state", "succeeded")
        span.set_attribute("agent.steps", 2)
        span.set_attribute("agent.tokens.reported", 18)
        # Prompt, answer, token, owner, session and tool arguments are omitted.
    spans = exporter.get_finished_spans()
    if len(spans) != 1:
        raise RuntimeError("expected one in-memory demo span")
    return {"name": spans[0].name,
            "attributes": dict(spans[0].attributes),
            "exporter": "in-memory"}


if __name__ == "__main__":
    print(capture_demo_span())
