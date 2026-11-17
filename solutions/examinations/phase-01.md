# Phase 1 reference defense and scoring

This is a reference architecture for grading, not a substitute for the learner's
independent build. The existing [API](../../forgeagent/api.py),
[storage](../../forgeagent/storage.py), and [search](../../forgeagent/documents.py)
provide tested mechanisms. To integrate retrieval, obtain owner-scoped text,
construct a Document with the validated identifier and text, then invoke pure
search under the same normalization policy. No network server is necessary to
demonstrate the application contract, and untrusted text never becomes Python code.

Use the phase problem's published point allocation. For system implementation,
award each subcategory only for independently executed behavior, including empty
and invalid cases. The provenance record must retain an identifier plus a measured
count, not an unsupported generated claim. Parameters prevent SQL injection;
owner-qualified predicates prevent cross-user leakage. These solve different flaws.

Failure expectations: malformed JSON rejects before write; other-owner GET returns
not found; an injected precommit exception rolls back; timeout propagates;
cancellation propagates and cleanup runs. If the write is offloaded to a thread,
a late commit is a known uncertain outcome requiring reconciliation, not evidence
the event-loop cancellation was ineffective. Do not award a claim that cancellation
“undoes everything.”

Numerical examples for defense: [[1,2],[3,4]] times [2,1] is [4,10]. Cosine of
[3,4] and [0,5] is .8. Derivative of (3x+1)² at 2 is 42; sweep h and state the
approximation/roundoff tradeoff. Square descent multiplies x by .8 at η=.1;
at η=1 it multiplies by −1 and fails to shrink. Softmax [0,ln2] is [1/3,2/3]
and invariant to shared shifts. With a 10% permanently failing group plus 90%
with independent .1 attempt failure, three-attempt total failure is
.1+.9×.1³=.1009. Simply cubing one marginal failure rate is unjustified.

For engineering defense require a diagram of ownership/effect boundaries,
thread-created connections, explicit local-only trust assumptions, a coherent
diff, and a measured quantity with workload/units. Identify missing production
controls: TLS, production identity lifecycle, admission limits, durable job queue,
revision checks, sandboxing, and operational monitoring. Listing them without
relating at least one to an actual failure mode is insufficient.

Critical failures cannot be compensated with math points. Retest a changed fixture
after remediation and preserve the first result. This is a cumulative educational
assessment, not a secure held-out agent benchmark; that benchmark remains a later
deliverable.
