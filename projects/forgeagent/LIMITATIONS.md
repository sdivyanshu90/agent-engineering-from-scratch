# Known limitations

- Lexical search is not syntax-aware or semantic, and a file-count cap can omit
  relevant files. Search scores are not confidence estimates.
- The path policy assumes an owned, non-adversarial workspace. It rejects
  symlinks during checks but does not eliminate hostile concurrent swap races.
- Repository reads may disclose private source to the provider. The caller must
  choose the authorized root; traces should not persist raw contents casually.
- The patch API is one-file whole-text replacement with size limits. It is not
  a multi-file transaction. Approval binding is not reviewer authentication.
- A restored proposal is unapproved and requires a fresh human review. A crash
  around writes can require operator reconciliation if the current hash is
  neither the expected before nor after digest.
- The opt-in Bubblewrap backend assumes Linux, Bubblewrap, system Python, and
  an owned workspace. It is tested for selected mount, network, and environment
  boundaries. It does not supply CPU or memory quotas or a multi-tenant security
  guarantee. Avoid placing credentials anywhere in the mounted workspace.
- Thread-offloaded synchronous MCP/backend work may outlive coroutine
  cancellation. External timeout and operation reconciliation are required.
- MCP schema support is deliberately narrow. Remote descriptions and content
  are untrusted. Read-only name allowlisting does not prove a remote tool's
  behavior is read-only; configuration must be reviewed.
- Context token estimates are heuristic, selection is lexical, and compaction
  loses information. Derived summaries do not inherit source authority.
- Offline scripted-provider fixtures measure deterministic protocol handling,
  not live-model coding quality, generalization, benchmark performance, or
  senior engineering experience.
- Visible development and held-out fixtures are small and can be contaminated
  if used for tuning. Results need case rows, denominators, and versioned splits.
- The teaching implementation does not provide an authenticated multi-tenant
  approval service, tamper-resistant audit store, or production deployment
  certification.
