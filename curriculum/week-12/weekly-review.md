# Week 12 weekly review

Reconstruct the complete state transition from task input to a verified result.
On paper, identify which component owns each decision: the provider proposes a
tool call; the runtime validates shape, policy, dependencies, and budgets; the
workspace checks paths and content revisions; a human authorizes one exact
proposal; an isolation backend executes a fixed test request; and the reviewer
decides whether evidence supports completion. Then trace one changed file
through its before hash, proposal hash, approval digest, apply, and test result.

## Retrieval prompts

1. Why does a lexical match count fail to establish code semantics?
2. Why is a file path a capability rather than an innocent string?
3. What exact fact does a SHA-256 compare establish, and what does it not?
4. Why must the approval channel be absent from the provider's tool registry?
5. Which runtime state is required to resume a pending tool call safely?
6. When is a compacted context summary weaker evidence than its source?
7. Why is a passing test command not proof of test isolation?
8. Which benchmark cases detect a system that always returns “done”?

## Remediation

If you cannot answer one prompt, revisit that day's lab and add a counterexample
to your notebook. A failed contract should lead to a narrower capability, a
better invariant, or a better measurement. Do not respond to poor task success
by silently granting a broader filesystem root, generic command execution, or
unreviewed writes. Re-run the fixed evaluation unchanged after any correction,
and retain the first report so the revision history remains interpretable.
