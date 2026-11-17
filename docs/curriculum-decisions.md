# Curriculum decisions

- Use the existing Git workspace as the repository root; its product/package
  name is `ai-agent-engineering-mastery`. Avoid a nested Git repository.
- Preserve 72 planned days but publish only actual authored chapters. Do not
  create empty phase folders or pretend a title list is content.
- Week 1 uses only the Python standard library. `unittest` avoids teaching a
  dependency manager and a test framework before functions. pytest can be
  introduced after core testing concepts; it is not currently required.
- Default Python is 3.12. The code declares 3.12–3.14 compatibility. Record
  exactly which interpreters were actually tested in the completion audit.
- The first CLI is intentionally lexical. A simple deterministic baseline
  supports later retrieval comparisons and makes model-free testing possible.
- Keep independent lab contracts smaller than the final reference. Explain
  differences, especially the Day 2 tokenization policy and Day 4 traversal.
- No live model calls, API secrets, background daemons, or cloud bills are
  required for this checkpoint. Modern API/protocol claims remain pending
  until their official sources and compatible versions have been verified.
