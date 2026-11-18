# Week 9 — Protocols, skills, and trust boundaries

**Days 49–54:** standard MCP stdio lifecycle and tools; path-scoped policy and approval-bound edits; Agent Skills format and progressive loading; an A2A conceptual comparison; and a composed capability audit.

This week implements a small offline **MCP 2025-11-25** stdio tools subset. It performs initialize/version agreement, `notifications/initialized`, `tools/list`, and `tools/call` with JSON-RPC line framing. It does not implement Streamable HTTP, OAuth, resources, prompts, sampling, elicitation, subscriptions, or A2A. The stdio client launches and owns its child process; that process generally runs with the client’s OS identity. This is not a sandbox.

The policy module applies only to an owned, stable workspace: bounded reads, relative-path and symlink checks, and one-use approval bound to session/tool/arguments/content hashes. These checks are not race-proof against hostile concurrent filesystem changes. Approval is an application/UI action and must never be registered as a model tool. `TestExecutor` delegates only to an explicitly supplied isolation backend and denies when none exists; a subprocess by itself is not isolation.

Skills are bounded text input, parsed with a deliberately minimal frontmatter subset and loaded progressively. Their contents never grant authority. A2A is discussed from its official specification only; there is no mock A2A implementation.

Run `python3 -m unittest tests.integration.test_mcp tests.security.test_policy` and `python3 labs/week-09/checks.py --day 1` through `--day 6` (with your submission module). Review the manifest for test coverage and limitations.
