# Week 1 — Review and remediation day

Do not add new features first. Check what can be reconstructed after a delay.

1. Closed book, draw source → process → values → output and explain assignment.
2. Normalize `"A,a! ... Agent"` by hand under Day 2's policy. Explain how the
   project's Unicode policy differs, and why mixing the two silently is wrong.
3. Write the counter from a blank file and prove its processed-prefix invariant.
4. Load temporary files in sorted order, including empty and invalid-UTF-8 cases.
5. Rank tied hits under a nonnegative limit without mutating caller data.
6. Run the CLI from a subprocess and inspect status, stdout, and stderr.
7. Take the [weekly exam](../../assessments/weekly/week-01.md) without solutions.

## Remediation by observed failure

- Counts wrong on whitespace: return to Day 1 and trace code points separately
  from split entries. Test empty, tab-only, and repeated-space input.
- Tokens vanish unexpectedly: return to Day 2; log each original and cleaned
  token in your owned fixture, then remove diagnostic output from product stdout.
- State leaks between calls: draw the object references from Day 3; allocate
  fresh local state, then retest call independence.
- Empty corpus hides a read failure: return to Day 4; separate `[]` from raised
  exceptions and verify the CLI's nonzero failure status.
- Ties depend on traversal order: return to Day 5; permute input and derive each key.
- JSON parse fails despite a visible answer: return to Day 6; keep stdout to
  the payload and stderr to diagnostics. Test from a fresh process.

Attempt a different fixture after remediation, not only the example whose answer
you remember. Pass all safety-critical criteria and score at least 80/100 before
marking the week mastered. Record unresolved gaps explicitly.

## Extension work while later weeks are authored

Add an optional extension filter with tests and documented uppercase behavior.
Measure repeated-query latency on fixed corpora. Propose (but do not prematurely
implement) an index: what changes when a file is edited? Write a one-page threat
model distinguishing owned local input from an untrusted multi-user service.
These tasks deepen Week 1; they do not replace the [Week 2 lessons](../week-02/README.md).

Review the count invariant after three days, CLI failure behavior after seven,
and all six contracts after fourteen. A calendar tick without reconstruction
evidence is not retention.
