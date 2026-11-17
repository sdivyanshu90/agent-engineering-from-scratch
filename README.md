# AI Agent Engineering Mastery

A first-principles learning program specializing in **Reliable AI Agent Systems
Engineering**: programming → model integration → retrieval → custom runtimes →
durable execution → security, evaluation, and production operations.

**Active build checkpoint, not a complete course:** Weeks 1–3 have eighteen
substantive chapters, eighteen independent labs, three weekly examinations,
a cumulative foundations exam, and tested reference code. Implementations include
the document CLI, storage-backed async API, scalar autograd, regression, a tiny
neural network and a character-language-model baseline. Weeks 4–12 and the
integrated coding agent remain unfinished. See [build status](docs/build-progress.json)
and [executed checks](docs/completion-audit.md).

Begin with [START_HERE](START_HERE.md), then follow the [roadmap](ROADMAP.md).
Each day has its own document, for example
[Week 1 / Day 1](curriculum/week-01/day-01/README.md) and
[Week 1 / Day 2](curriculum/week-01/day-02/README.md), and
[Week 2 / Day 1](curriculum/week-02/day-01/README.md).

The intended learner starts with no programming background. Experienced learners
can use the [diagnostic](assessments/diagnostic/README.md), but must demonstrate
implementation and debugging rather than recognize vocabulary. The intensive
plan has 72 instructional days at 7–9 focused hours each (504–648 hours), plus
12 review days. Complete beginners may need several additional weeks. This
program does not confer years of operational experience or guarantee seniority.

Use Windows, macOS, or Linux; Python 3.12 is the teaching default (3.12–3.14
supported), Git, a terminal, and a text editor. Week 1 needs only a modest CPU
laptop, approximately 1 GB free disk space for tooling, and no model API or GPU.
Later CPU mathematics must remain small. Optional hosted-model experiments will
need explicit configuration and may incur charges; none is needed now.

```sh
python scripts/check_environment.py
python -m forgeagent.cli datasets/sample-data agents
python -m unittest discover -s tests -v
```

Run from the repository root after selecting your Python environment. Lab
checks are in each week’s `checks.py`; use `--module` to test your own attempt.
`python scripts/validate_exercises.py` checks all authored references.
Keep answers separate in `solutions/` until you have tried independently. Record
test evidence, exam scores, and delayed retention in [PROGRESS_TRACKER](PROGRESS_TRACKER.md).

| Where | What is actually present |
|---|---|
| [curriculum](curriculum/README.md) | Week/day navigation and eighteen authored chapters |
| [labs](labs/week-01/README.md) | Runnable starters, contracts, hints, and public checks |
| [solutions](solutions/labs/week-01/explanation.md) | Independent reference code and reasoning |
| [assessments](assessments/weekly/week-01.md) | Diagnostic, daily questions within chapters, weekly exam |
| [projects](projects/python-cli/README.md) | ForgeAgent milestones 1–2: local inspection and persistent API |
| [resources](RESOURCE_LIBRARY.md) | Small verified primary-source set and verification limits |
| [docs](docs/build-progress.json) | Build status, audits, standards, coverage, continuation plan |
| [scripts](scripts/validate_curriculum.py) | Checkpoint integrity and explicit full-completion mode |
| [tests](tests/integration/test_documents.py) | Reference behavior, process contracts, examples, and boundaries |

ForgeAgent grows through one codebase, `forgeagent/`. Its current CLI and
owner-scoped storage API are real components, not a coding agent. Provider
adapters, retrieval indexes, custom agent loop, durable execution state, MCP,
controlled patches, isolated execution, production service infrastructure, and
containerization are planned future milestones. No agent framework hides
or implements the future core runtime.
