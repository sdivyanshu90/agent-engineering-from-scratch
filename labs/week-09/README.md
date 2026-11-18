# Week 9 labs — protocols, skills, and trust boundaries

Each day has one deterministic function contract in `starter/tasks.py`. Implement the requested function without network access, then run `python labs/week-09/checks.py --day N --module path/to/tasks.py`. The public checker accepts `check(day, path=None)` and does not import solutions unless no module path is supplied. These checks cover small contracts, not security certification.

1. Parse a tool result and preserve protocol errors as non-success.
2. Normalize a skill identifier and reject traversal or invalid separators.
3. Bind a one-time approval to owner/session, tool, exact arguments, and content revision.
4. Validate a small agent identity/capability manifest without duplicate entries.
5. Hash exact bytes for optimistic concurrency.
6. Enforce a tool allowlist before dispatch.

Run one lab at a time; all fixtures are local. The repository implementation and isolated subprocess tests are in `forgeagent/` and `tests/`. A passing public check means the specified examples pass; reviewers should add adversarial cases.
