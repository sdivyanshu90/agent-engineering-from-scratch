# D69 — Patch proposals and human authority

## 1. Learning objectives

Design a patch workflow where a proposal is inert until a human approves the
exact content, and where that approval can be consumed only once. Bind the
proposal to a workspace session, tool name, path, original SHA-256, and
replacement digest. Demonstrate that a changed source file invalidates the
proposal, an altered review digest cannot authorize it, and a second apply is
rejected. Explain why the model must not receive `approve_patch` as a tool and
why a signed or typed approval does not establish that the patch is correct.
Your acceptance evidence is a table of approve/reject attempts against the same
proposal plus the resulting file hash and one-use state.

## 2. Required prerequisites

Complete D68 and read the concrete Week 9 `Workspace.propose_patch`,
`approve_patch`, and `apply_approved` methods. Review the schema and dispatch
behavior in `runtime.py`; write-effect tools are denied unless the caller
explicitly passes `allow_write=True`. Know SHA-256 at the byte level and know
that JSON binding needs a canonical encoding if its digest is used. Understand
the difference between access control and review quality: a correctly bound
approval says which bytes were accepted by which session, not that those bytes
are secure. This lesson assumes the workspace is owned and non-adversarial; the
filesystem checks are not an OS-level defense against hostile concurrent link
swaps. For production, the proposal store and approval identity need durable,
authenticated ownership.

## 3. Problem motivation

Text generation is easy to mistake for an action. If a coding model both
proposes and applies its own patch, the user cannot meaningfully review a
change; any wording in the model's answer can become an implicit grant of
authority. A separate approval channel creates a moment when a person can inspect
the precise diff and decide. But “approve proposal 17” is still underspecified
if the source changed, the target path was swapped, or proposal 17 was rebound
to another replacement. A safe approval must name the exact object under
review. It also must be one-use so a stale authorization cannot be replayed
after another state transition. The policy should reject uncertainty rather
than guessing which object the user meant.

## 4. Intuitive explanation

Imagine signing a printed change request with the page count and a fingerprint
of every page. If someone replaces page two after you sign, the fingerprint
does not match. If someone tries to use the same signature twice, the clerk
marks it consumed. The model may prepare the form and explain it, but it cannot
sign its own form. A reviewer should see the original text, the proposed text,
the path, and a concise change summary. The approval token then points back to
that exact proposal. If any relevant value changes, the token no longer fits.
This does not mean the reviewer knows the patch is correct; it means the system
can prove which patch they chose to authorize.

## 5. Deep technical explanation

The Week 9 workspace stores a proposal with an internal random identifier and a
binding object. The binding includes `session`, `tool`, `arguments`, `path`,
`revision`, and the SHA-256 of the replacement text. `approve_patch` checks that
the supplied session, tool, and arguments equal the proposal's original
binding. `apply_approved` checks the same binding again, confirms the proposal
is approved and unused, re-resolves the path, and compares current file bytes
to the original revision. The proposal is marked used before the one-file write.
This sequence narrows replay and stale-edit risks. It is not a transaction over
multiple files, and a crash can leave the caller uncertain whether the write
completed. Durable operation intent and reconciliation belong to the next
system layer. The model-facing registry exposes `propose_patch` as a write
proposal gated by runtime policy, but approval remains a method invoked only by
the human-facing application path.

The UI must display the content being approved, not just a digest or generated
summary. A digest helps bind the selection, but people cannot meaningfully
inspect an opaque hash. An approval receipt can include proposal ID, path,
before digest, after digest, reviewer identity, timestamp, and decision. It
should not contain hidden alternate text. A UI should derive visible contents
from the protected proposal record and render escaped text; otherwise source
markup could spoof a confirmation screen. The authorization callback should
verify a review digest generated from canonical fields and should keep the
proposal bytes server-side. This capstone's helper uses a local digest as a
teaching seam, not as authentication against a malicious caller.

## 6. Mathematical foundations

Let \(x\) be the original bytes and \(y\) the replacement bytes. The proposal
records \(h_x=H(x)\) and \(h_y=H(y)\). Approval is a predicate over the tuple
\(B=(session,tool,args,path,h_x,h_y)\). Apply is permitted only when the
current file \(x'\) satisfies \(H(x')=h_x\), the approval refers to the same
\(B\), and the proposal state is approved and unused. After writing, verify
\(H(y')=h_y\), where \(y'\) is reread from disk. This protects against stale
state assuming the hash function behaves as intended. It does not provide
cryptographic identity for the human unless the approval channel authenticates
that person and protects its secret. A plain equality check inside a local
process is not a signature scheme. One-use state is a finite-state machine:
`proposed → approved → used`, with rejection or stale transitions terminal for
that proposal.

## 7. Architecture and execution diagrams

The provider can request a proposal, but cannot move the proposal into approved
state. The user interface retrieves exact details and sends a review action to
the policy layer. The policy checks the original bytes immediately before the
write. If an approval or path check fails, the application reports a bounded
reason and preserves the original file. Never silently rebase a proposal onto
new source bytes: that would authorize content the reviewer did not see.

```mermaid
stateDiagram-v2
    [*] --> Proposed: model proposes exact replacement
    Proposed --> Rejected: human rejects
    Proposed --> Approved: human reviews exact bytes and bound digest
    Approved --> Stale: current file hash changed
    Approved --> Applied: binding matches; one-use apply
    Applied --> [*]
    Rejected --> [*]
    Stale --> [*]
```

## 8. Implementation from first principles

First calculate the original hash over UTF-8 bytes; do not normalize line
endings after the hash. Store replacement text exactly as reviewed. Create a
canonical review record that excludes unstable formatting and includes both
the before and after digests. The review surface must also render the actual
replacement bytes so a person can inspect semantics. On approval, compare the
review digest, then call the policy method with the exact original session,
tool, and arguments. Apply rechecks the source revision. The model never
receives this approval callback in its tool registry. Here is the local digest
calculation used by the capstone helper; it is a binding aid, not a credential.

```python
import hashlib, json

def review_digest(path, before, after):
    record = {"path": path, "before": before, "after": after}
    canonical = json.dumps(record, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode()).hexdigest()
```

## 9. Worked execution walkthrough

The fixture contains `counter.py` with bytes `b"count = 0\n"`, digest `h0`.
The agent proposes `b"count = max(0, count)\n"`, digest `h1`, under session
`demo-4`. The review page shows the complete before and after text and displays
`review_digest("counter.py", h0, h1)`. A reviewer sends approval for that exact
digest. Before apply, another process changes the file to `count = 1`; its hash
is `h2`. `apply_approved` compares `h2` to `h0` and rejects stale content. The
reviewer must ask for a new proposal. On a fresh fixture, approval succeeds,
the resulting file hashes to `h1`, and the proposal cannot be applied again.
Attempting to approve the same ID under another session fails the binding
check. Attempting to edit the replacement after approval also changes the
argument binding. Each result is a separately observable rejection, not a
silent rewrite. This trace demonstrates exact authorization, not that the
clamping logic is the right product behavior.

## 10. Independent laboratory

D69 asks you to exercise the real policy object in a temporary directory. Create
one source file, record the original hash, propose a replacement, and produce
the exact visible review packet. Test rejection for a wrong review digest,
wrong session, changed source, second approval after use, second apply, and
modified tool arguments. Then verify success on a fresh proposal. Keep tests
separate so one rejection does not consume a proposal required by another case.
Your public check uses an isolated test directory and never changes a
repository file. Document that the user action is represented by a direct
review callback in this local exercise; it is not authentication. Add a short
threat-model section explaining which fields must be protected if the proposal
store becomes a network service.

## 11. Experiments

Compare three approval designs against the same six adversarial mutations:
proposal ID only, proposal ID plus review digest, and the full policy binding
with one-use state. Track which mutations each design rejects. Include a
modified path, altered replacement, changed source, wrong session, repeated
apply, and path symlink. The digest-only variant can bind bytes while still
failing to authenticate the human. Explain how a visible diff and authenticated
reviewer identity address different properties. Do not infer security from
zero failures in six handpicked cases; list the cases and assumptions. Also
measure review packet size for a 10-line and 1,000-line replacement and discuss
how the UI can preserve inspectability without replacing the full diff by a
model summary. A digest summary can supplement review, never substitute for the
content selected for approval.

## 12. Failure analysis

The UI can display the wrong proposal while sending the right ID, or display
the right proposal but call apply with different arguments. A local digest
alone does not prevent a malicious application from forging a reviewer action.
The filesystem can change between check and write under hostile concurrency;
the class explicitly limits its assumption to an owned, non-adversarial
workspace. A process can crash after bytes are written but before reporting
success. An approval can be stranded if the proposal store is only in memory.
Multiple files can be partially applied because this interface is one-file
only. A symlink race is not solved by string path validation. Do not add
automatic retry or rebase to “make it work”; use a new review cycle or explicit
reconciliation. These are design boundaries that a service deployment must
address with authenticated identities, durable records, locked file handles,
and/or isolated snapshots.

## 13. Engineering tradeoffs

Whole-file replacement is simple to bind but scales poorly for large source
files and can obscure small changes. A patch format is more reviewable and
supports line context, but parsers must reject ambiguous hunks and bind to the
exact base revision. The teaching policy uses replacement text with a 64 KiB
cap. Multi-file atomic commits require a transaction mechanism such as a
content-addressed worktree or version-control commit; sequential writes can
partially succeed. Keeping proposals in memory makes the example small, but
requires durable persistence before a reviewer can approve asynchronously.
One-use approval reduces replay but recovery must distinguish consumed from
unknown after a crash. The design should choose a simple explicit terminal
state and offer operator reconciliation rather than claiming exactly once.

## 14. Real-world connection

Package upgrades, infrastructure plans, migrations, and generated configuration
all benefit from approvals bound to exact artifacts. In a deployment pipeline,
the artifact digest is often more stable than a human-readable branch name.
However, secure approvals also require reviewer authentication, role policy,
separation of duties, expiry, audit logs, and a protected channel. The exact
human-readable diff remains important because a content digest alone is not
meaningful to a reviewer. In collaborative code review, the base commit and
patch commit provide revision identities; a merge should be blocked if the
base moves and review no longer applies. The same principle underlies signed
release artifacts: trust attaches to a concrete object and an accountable
actor, under explicit verification rules.

## 15. Common misconceptions

“The reviewer approved the task” is broader than “the reviewer approved this
replacement for this revision.” “A content hash authenticates the person” is
false; it identifies bytes. “The diff passed tests” does not show the tests ran
after apply on those bytes. “One-use means crash-safe” is false without durable
state and reconciliation. “The model cannot call the approve tool, so the UI
is secure” ignores compromised callers and forged sessions. “Path containment
is a sandbox” confuses process authority with a library check. “A generated
change summary is enough to approve” hides changes and prompt manipulation.
Finally, “stale proposals can be rebased automatically” undermines exact
approval. Bind identity and content, then make reviewers inspect the full
artifact they authorize.

## 16. Technical examination

For a given proposal, list every field that must match at approval and apply.
Explain why both the original and replacement digests appear in a review
packet. Construct a stale-source race and state what the policy rejects. State
what happens if apply writes bytes but the process dies before returning. Draw
the difference between a one-file proposal and a multi-file transaction. Then
design a durable approval receipt with reviewer identity, timestamp, expiry,
and proposal binding. Identify which fields are security-sensitive and how an
unauthenticated local method differs from a signed identity assertion. Finish
by naming one property that the approval protocol cannot provide: correctness,
availability, or absence of bugs in the OS. Defend your answer precisely.

## 17. Daily mastery gate

Pass only if approval cannot be invoked through the model's tool registry,
wrong binding values reject, stale content rejects, and a successful proposal
is applied once. The before and after hashes in the review packet must match
independently computed hashes. Your explanation must separate content binding
from human authentication and correctness review. If you fail, keep the failing
case as a regression fixture and refine the proposal state machine. Do not
weaken the binding to make the test pass. The gate establishes that the local
policy behaves according to its narrow contract; it does not certify the
review UI or protect against malicious concurrent filesystem mutation.

## 18. Resources

Primary material is `forgeagent/policy.py`, the D68 trace, and the local
`hashlib`/`json` standard-library docs. Read the code's own warning about
non-adversarial workspaces and the limited race protection. Compare its binding
fields against the threat model you write. You do not need a cryptography
library or external service to complete this lab. If you consult formal
cryptographic references, distinguish collision resistance from digital
signature authenticity; they solve different problems. Record all assumptions
in your report. An approval callback exercised inside the same process is a
functional test of equality conditions only. It is not evidence that a
production identity provider, browser, or audit log is correctly secured.

## 19. Revision and retention

From memory, redraw the proposal state machine and annotate the transition that
checks the current file hash. Recreate the wrong-session and stale-file cases
without consulting the implementation. Then revisit your experiment and point
out one authorization property not measured by your six mutations. After a
week, explain why an after-hash and reviewer identity answer different
questions. Keep your review packet narrow but complete: path, exact diff,
revision, and scope. If your notes say “the hash approves the code,” rewrite
them to distinguish identifying content from judging content.

## 20. Next lesson connection

An approved patch still needs testing, and test commands execute code. The next
lesson moves authority from a human-reviewed write into a separate execution
environment. You will see why an explicit test backend is required, why a
fixed argv is safer than a model-supplied command, and why a subprocess on the
same machine is not automatically isolated. Carry today's content digest into
the test trace so results can be associated with the exact applied tree.
