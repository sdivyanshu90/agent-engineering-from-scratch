# Week 7 labs: bounded runtime

Each day has an incomplete but importable starter in `starter/dayNN.py`. Work
independently of `solutions/labs/week-07`; the public contract is runnable with
`python labs/week-07/checks.py --day N --module labs/week-07/starter/dayNN.py`.
From the repository root, omit `--module` to inspect the completed reference.
The checker deliberately covers only a few boundary cases.

1. **Control flow:** implement explicit classification to a workflow, agent, or
human review state. Document what makes a workflow's route fixed and which
transition remains guarded. Add one unseen task classification fixture.
2. **Typed capability:** implement exact key/type/range validation for the
closed scalar subset. Add a handler counter and prove invalid arguments never
reach it. Explain why an allowlist and schema do not sandbox the handler.
3. **Custom loop:** implement finish and calls decisions over deterministic
JSON fixtures. Preflight an entire batch before executing its first call.
Append bounded observations and demonstrate an invalid later call has no
earlier side effect.
4. **DAG scheduler:** return stable topological layers. Test empty graph,
independent nodes, a chain, a missing parent, a cycle and a failed prerequisite.
Discuss why concurrent writes need stronger coordination than this lab.
5. **Budget accounting:** reconcile usage after each completed model response.
Demonstrate the reported total can exceed the limit and blocks the next action;
explain why that does not enforce provider-side spend.
6. **Trace summary:** report lifecycle counts, terminal state and stable failure
categories without copying prompt or tool payloads. Add malformed event tests
and choose a redaction policy for production traces.

## Graduated hints

Start by stating the function's invariants in comments. Then implement the
success path and run one contract. Next enforce exact types (`bool` is a Python
subclass of `int`, so check `type(x) is int`). Add rejection before side effects.
Finally create tests for malformed, boundary, and failure cases, then explain
what your tests cannot establish. The solution files are executable references;
`solutions/labs/week-07/explanation.md` discusses their design and limits.
