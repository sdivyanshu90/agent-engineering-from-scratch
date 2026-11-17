# Contributing

Read [technical standards](docs/technical-standards.md) and the
[build manifest](docs/build-progress.json) before adding content. Work in scheduled
order unless fixing a prerequisite defect. Never mark a chapter complete from
its headings or word count alone. A chapter needs original teaching, a trace,
a runnable example, an independent lab, separate solutions, assessments, and
actual validation evidence.

Use `curriculum/week-NN/day-NN/README.md` and preserve stable D01–D72 identifiers.
Add concept coverage and prerequisite edges in the manifest. Keep learner starters
runnable but incomplete, with explicit expected failing contract checks. Ordinary
CI must run references, not treat unfinished learner files as correct.

Before proposing a change run:

```sh
python scripts/validate_curriculum.py
python scripts/validate_links.py
python scripts/validate_exercises.py
python -m unittest discover -s tests -v
```

Run `python scripts/validate_curriculum.py --require-complete` only as the final
product gate; it intentionally fails while planned work remains. Checkpoint CI
must not obscure this distinction. Record commands, outcomes, interpreter, source
verification limitations, and pending work in the audit and build log. Never
manufacture benchmark outcomes or update criteria to make an existing result pass.

Add sources selectively. Distinguish stable foundations from version-sensitive
APIs; pin compatible dependencies before publishing integrations. Keep tests
CPU-sized and offline by default. Separate optional live evaluations and disclose
cost controls. Review security claims against actual boundaries rather than
function names such as “safe.”
