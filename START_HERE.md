# Start here

This checkpoint supports the first four weeks. The remaining eight weeks are
planned, not ready to study. See [the roadmap](ROADMAP.md) for the learning order
and [the audit](docs/completion-audit.md) for exact verification evidence.

## 1. Install prerequisites

Install Python 3.12, Git, and an editor. On Windows use the Python installer
with the PATH option; verify with `py -3.12 --version`. On macOS/Linux use
`python3.12 --version` after installing Python through your preferred trusted
installer/package manager. `git --version` checks Git. A terminal accepts the
commands below; a Python prompt (`>>>`) accepts Python expressions instead.
No administrator privileges should be needed to run repository exercises.

## 2. Get the repository and choose its root

The verified remote is public. Clone with
`git clone https://github.com/sdivyanshu90/agent-engineering-from-scratch.git ai-agent-engineering-mastery`,
then `cd ai-agent-engineering-mastery`.
In the provided workspace the root is already
`/home/somu/agent-engineering-from-scratch`; open a terminal there instead.
Check that your editor shows this file alongside `pyproject.toml`.

## 3. Select a Python environment

Recommended when uv is installed (see [official installation guidance](https://docs.astral.sh/uv/getting-started/installation/);
that installation page is supplementary and not part of the verified set):

```sh
uv python install 3.12
uv sync --locked
uv run python scripts/check_environment.py
```

The project currently has no third-party dependencies. The lock captures an
empty dependency graph. After setup you may prefix any `python` command here
with `uv run`, avoiding shell-specific activation.

A standard-library alternative needs no dependency manager. On Linux/macOS:

```sh
python3.12 -m venv .venv
source .venv/bin/activate
python --version
```

On Windows PowerShell:

```powershell
py -3.12 -m venv .venv
.venv\Scripts\python.exe --version
```

For subsequent Windows commands replace `python` with
`.venv\Scripts\python.exe`, or activate with `.venv\Scripts\Activate.ps1` if your
shell policy permits. No need to weaken system-wide script policy. Python 3.13
and 3.14 are supported alternatives; use that version consistently. A virtual
environment keeps this project's tools separate from other projects.

## 4. Check the environment

```sh
python scripts/check_environment.py
```

Expect `Python 3.12: ready; no API key required` (version number matches your
interpreter). If the root assertion fails, change directory to the repository.
If `python` is not found, use the selected interpreter's full path.

## 5. Run the first educational example

```sh
python -m forgeagent.cli datasets/sample-data agents
```

Expect `[{"path": "agents.txt", "count": 2}]`. This searches two local text
files. You need not understand all its internals yet; Week 1 builds them.

## 6. Run the first test

```sh
python labs/week-01/checks.py --day 1
```

Expect `Day 1: public contract passed`. This checks the reference. Later use
`--module` to select your own file. For all repository reference tests:

```sh
python -m unittest discover -s tests -v
```

A test runner showing zero tests is not a meaningful pass.

## 7. Open Day 1

Read [Week 1 / Day 1](curriculum/week-01/day-01/README.md). Execute the example,
then close the page and predict a new input before checking it.

## 8. Complete the first independent assignment

Using your editor, create `learner-work/week-01/` and copy
[labs/week-01/starter/summary.py](labs/week-01/starter/summary.py) into it. The
starter runs but does not yet satisfy the contract. Implement the required
summary, then run:

```sh
python labs/week-01/checks.py --day 1 --module learner-work/week-01/summary.py
```

If it fails, inspect actual and expected counts. Use the graduated
[hints](labs/week-01/hints.md) only after attempting the trace. Keep your own
code separate from reference solutions.

## 9. Record completion

In [PROGRESS_TRACKER](PROGRESS_TRACKER.md), record the date, command/output,
exam score, misconception corrected, and planned delayed review. A public-test
pass alone is not mastery: meet Day 1's explanation and unseen-input gate.

## 10. Continue by gates

Follow Days 2–6 in [Week 1](curriculum/week-01/README.md), then the review and
weekly exam. Remediate weak areas before moving on. Then follow [Week 2](curriculum/week-02/README.md) through its review and
phase examination. Continue with [Week 3](curriculum/week-03/README.md) after the foundations gate. Continue with [Week 4](curriculum/week-04/README.md) and the model-internals phase gate. Weeks 5–12 appear in the [full schedule](CURRICULUM.md) as
planned titles; they currently have no lesson files. The next authoring step is recorded in the build manifest.

No paid services are required. Never place API keys in tracked files. Optional
live-model instructions and explicit usage-cost controls must be authored before
later model experiments are considered ready.
