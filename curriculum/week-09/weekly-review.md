# Week 9 weekly review

Draw two flows from memory. The first is an MCP stdio session: client-owned process launch, initialize request, version and capability result, initialized notification, tools/list, tools/call, content/isError response, then close. Mark the JSON-RPC request IDs and the notification that has no ID. The second is a proposed edit: owned root, bounded read, path validation, base hash, exact arguments, human approval, current-hash recheck, one-use write, and explicit external isolation backend for tests.

Then compare an Agent Skill and an A2A Agent Card. Both help describe capabilities, but neither grants this host permission to disclose files or execute code. Skill body/reference text remains untrusted. A remote card also introduces endpoint identity and authentication questions; A2A task state may outlive the initial request. This repository’s A2A section is conceptual.

## Retrieval prompts

- Which bytes are a frame on stdio, and where may diagnostics go?
- What does a capability advertisement establish, and what does it not establish?
- Which identities and fields bind a patch approval? What makes it stale?
- Why does a correct workspace path check not equal an OS sandbox?
- Which Skill fields are required, and why does `allowed-tools` metadata not enforce runtime authorization?
- Which asynchronous A2A concepts are absent from a one-shot MCP tools/call?

## Remediation

If lifecycle order is unclear, reproduce the subprocess transcript and annotate each transition. If transport scope is unclear, contrast stdio child ownership with HTTP endpoint deployment and its separate origin/authentication requirements. If policy scope is unclear, mutate the file after approval and retry with changed arguments; both must deny. If skill trust is unclear, put a request for shell execution in the sample body and verify it changes no allowlist. If A2A is unclear, use the official specification to trace one task from send through terminal state and artifact retrieval, without inventing local endpoint behavior.
