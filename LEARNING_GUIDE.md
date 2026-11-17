# Learning guide

Learn by predicting, implementing, observing, and correcting. Before running an
example, write the next state on paper. A mistaken prediction is useful evidence:
find the rule it contradicted and test a different input. Rerunning a familiar
example until it feels comfortable is weak evidence of understanding.

Read the motivation and intuition first, then trace the technical mechanism.
Execute the example once, close it, and reconstruct it in a fresh file. Attempt
the independent lab from its contract. If stuck, use the conceptual hint before
the algorithmic hint, then the implementation hint. Consult the reference only
after a sincere attempt and a written description of the obstacle. After reading
it, close it and solve a changed input independently.

Debug the first wrong state, not only the final error. Reduce a failure to the
smallest fixture, predict its correct result, reproduce the defect, make one
reasoned correction, and retain a regression test. Keep side effects in temporary
owned directories. Do not fix errors by hiding exceptions or disabling validation.

Your notes should record a contract, a trace, an invariant, one counterexample,
and a design tradeoff. For measurements record units, input sizes, interpreter,
repetitions, and variability. A statement such as “faster” needs a workload and
numbers. Distinguish source evidence, your inference, and remaining uncertainty.

Use active recall after one, three, seven, and fourteen days. Reconstruct before
rereading. On review days take exams without answers, then remediate by failure
category. A failing test does not mean you learned nothing; an unexplained green
test does not mean you mastered the mechanism.

AI assistance can ask probing questions, interpret an error after you have traced
it, or suggest a new counterexample. Do not delegate the implementation that is
being assessed. Record assistance, explain every submitted line, and reproduce
the mechanism without the assistant. When changing an architecture, defend it
against a plausible alternative with correctness, latency, memory, security,
and maintenance evidence.

Follow [the roadmap](ROADMAP.md), extend the calendar when gates fail, and keep
[learner progress](PROGRESS_TRACKER.md) separate from repository build progress.
