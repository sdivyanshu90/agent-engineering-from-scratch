# Graduated hints

| Day | Conceptual | Algorithmic | Implementation |
|---|---|---|---|
| 1 | Completion envelope and task correctness differ | Validate status then supported content then usage | Preserve roles in payload; reject refusal instead of returning empty text |
| 2 | Data must not become trusted instructions | Build two ordered messages, canonicalize all request fields | asdict, sorted object keys, fixed JSON separators, UTF-8 SHA-256 |
| 3 | Parsing is only the first gate | Byte cap, unique keys, exact fields, value constraints | Check type(urgent) is bool; reject blank summaries |
| 4 | A prefix is not a final value | Collect under total bound, require terminal state | finally closes generator; never catch cancellation as retryable |
| 5 | All attempts share one deadline | Classify error, finite attempts, backoff before another | Keep asyncio.timeout outside loop and inject sleep |
| 6 | Prices need explicit units | Multiply counters by per-million rates, divide once | Decimal from strings; reject non-finite/negative rates |
