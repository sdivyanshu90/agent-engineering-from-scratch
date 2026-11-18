# Frequently asked questions

**What is available?** All 72 chapters with labs, references and exams, plus
the ForgeAgent capstone. See the [completion audit](docs/completion-audit.md).

**Where is Week 1 / Day 1?** [Here](curriculum/week-01/day-01/README.md).
Every authored day has a separate document. [ROADMAP](ROADMAP.md) explains order.

**Must I finish in twelve weeks?** No. Pass gates and extend when necessary.
The schedule is highly intensive and not an experience or employment guarantee.

**Do I need paid APIs or a GPU?** The CPU labs and scripted tests run without either. Hosted model
experiments can incur usage charges.

**Why not use an agent framework?** The specialization requires understanding
state transitions, tools, budgets, persistence, and failures directly. Later
comparisons can follow an independent implementation.

**Why does my starter fail?** It is runnable baseline behavior, not a completed
solution. Implement the contract and use `--module` to select your attempt.
Reference tests pass separately; they do not grade your personal understanding.

**Why does `a-b` tokenize differently in two examples?** The Day 2 lab preserves
internal punctuation; the integrated project selects Unicode alphanumeric runs.
These are two explicit contracts. Query and document processing inside one
search system must use the same policy.

**Why not catch every error?** That can turn an unreadable corpus into a false
empty success. Expected operational failures should become explicit UI errors;
unexpected defects should remain diagnosable.

**Does rejecting links make search safe for strangers?** No. It assumes a stable,
owned local workspace and has check/open races and no OS isolation. Read the [isolation and workspace boundaries](projects/forgeagent/LIMITATIONS.md)
before choosing a test backend.
