# Resource verification ledger

Retrieval date: 2026-11-17 (workspace clock). Eight pages were opened and their
content inspected using web retrieval after the Firecrawl scrape endpoint
reported `Unknown tool`. A search returned no relevant results. External page
anchors were not independently fetched, but named chapter sections were inspected
where surfaced. This ledger does not assert that all sources represent the
latest available version: the Python tutorial is explicitly version 3.12.

All eight sources are publicly accessible without a paid account. Reading times
below are planning estimates, not measured learning outcomes. Explanations in
this repository are original; external pages remain supplemental references.

| Title / organization | Verified URL and section | Prerequisites | Lesson | Use and expected outcome | Study estimate |
|---|---|---|---|---|---|
| Informal Introduction / Python Software Foundation | https://docs.python.org/3.12/tutorial/introduction.html — 3.1 numbers, text, lists | D01 local explanation | D01 | Practice expression evaluation and distinguish strings from printed representation | 25 min |
| More Control Flow Tools / PSF | https://docs.python.org/3.12/tutorial/controlflow.html — if, for, range, defining functions | D01; D02 before function sections | D02–03 | Trace branches/loops and explain parameters/returns | 50 min |
| Data Structures / PSF | https://docs.python.org/3.12/tutorial/datastructures.html — list methods, tuples, sets, dictionaries | D02 | D02–03 | Select a collection by behavior and recognize mutating methods | 40 min |
| Input and Output / PSF | https://docs.python.org/3.12/tutorial/inputoutput.html — 7.2 reading and writing files | D03 | D04 | Use explicit encodings and understand resource cleanup | 25 min |
| Errors and Exceptions / PSF | https://docs.python.org/3.12/tutorial/errors.html — 8.1–8.4 | D03 | D04 | Distinguish parsing errors and runtime failures; handle narrowly | 25 min |
| Classes / PSF | https://docs.python.org/3.12/tutorial/classes.html — scopes, namespaces, classes | D03–04 | D05 | Explain instance data, methods, and shared state hazards | 30 min |
| unittest / PSF | https://docs.python.org/3.12/library/unittest.html — basic example, assertions, discovery | D05 class introduction | D05–06 | Write independent expected-value tests and verify discovery | 45 min |
| Working on projects / Astral | https://docs.astral.sh/uv/guides/projects/ — project structure, lockfile, execution | Terminal setup | Onboarding/D06 | Select the environment consistently and distinguish dependencies from source | 20 min |

## Pending verification

The uv installer URL in onboarding is provided as supplementary installation
navigation; that page was not in the inspected eight-page set. No Git, argparse,
dataclasses, regex, provider API, or modern protocol documentation has been
recorded as verified yet. The local standard-library examples are tested; this
is distinct from a documentation-link verification claim.

Before later chapters use changing APIs or protocols, retrieve the official
specification, record date/version, pin implementation dependencies, and test
negotiation/error paths. A tutorial describing a protocol does not establish
November 2026 compatibility. No latest MCP/A2A/provider version is claimed here.

## Week 2 selected primary sources — retrieved 2026-11-17

Same public/free access model and estimated-time caveat as above. Seven additional
selected pages bring the primary set to fifteen. An MDN HTTP overview was also
inspected but not selected as the authoritative technical basis; the IETF RFC
provides that basis. No externally hosted content was copied into chapters.

| Title / organization | Verified URL / specific section | Prerequisite and lesson | Use / expected outcome | Estimate |
|---|---|---|---|---|
| HTTP Semantics / IETF, Fielding et al. | https://www.rfc-editor.org/rfc/rfc9110.html — terminology, methods, status codes, idempotent methods | Week 1; D07/D10 | Separate message representation, methods, authentication and retry assumptions | 50 min targeted |
| JSON / Python Software Foundation | https://docs.python.org/3.12/library/json.html — decoder hooks, untrusted-input caution | D07 local explanation | Validate exact shapes and reject ambiguous duplicate fields | 20 min |
| sqlite3 / PSF | https://docs.python.org/3.12/library/sqlite3.html — placeholders, contexts, transaction control | D07; D08 | Parameterize values, commit/rollback, close separately | 45 min |
| Coroutines and Tasks / PSF | https://docs.python.org/3.12/library/asyncio-task.html — TaskGroup, cancellation, timeout, to_thread | D08; D09/D10 | Own concurrent work and explain cooperative stopping | 80 min |
| Streams / PSF | https://docs.python.org/3.12/library/asyncio-stream.html — readexactly, drain, close | D09 | Distinguish byte-stream framing from application messages | 25 min |
| Gradient descent / Google ML Crash Course | https://developers.google.com/machine-learning/crash-course/linear-regression/gradient-descent — update mechanism | D11/D12 local math | Connect downhill steps to trainable parameter updates | 30 min |
| Sigmoid / Google ML Crash Course | https://developers.google.com/machine-learning/crash-course/logistic-regression/sigmoid-function — exponential probability map | D12 | Compare binary normalization with categorical softmax | 20 min optional |

A dedicated freely accessible vector/probability source and a calculus supplement
remain unselected; the chapters include the necessary local explanation and
exercises. Remaining-phase research still needs the sources listed in the library.
Google's broad convergence language must not be interpreted as a guarantee for
arbitrary learning rates or nonconvex neural losses; local lessons state the
actual assumptions of each toy example.

## Mathematical supplements — selected 2026-11-17

Three MIT OpenCourseWare session pages were retrieved and inspected, bringing
the selected source-page count to eighteen. Verification covers the pages and
visible instructional/resource navigation; it does not assert that linked
lecture videos were watched in full or every linked PDF was downloaded.
All are free/public and optional reinforcement after the local derivations.

| Title / author | Verified session URL | Prerequisites / lesson | Why useful and expected outcome | Estimate |
|---|---|---|---|---|
| Geometry of Linear Equations / Gilbert Strang, MIT 18.06SC | https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/pages/ax-b-and-the-four-subspaces/the-geometry-of-linear-equations/ | D11 arithmetic/algebra | Geometric interpretation of rows/columns and equation systems; connect shapes to numerical operations | 45 min optional |
| Probability Models and Axioms / John Tsitsiklis, MIT 6.041SC | https://ocw.mit.edu/courses/6-041sc-probabilistic-systems-analysis-and-applied-probability-fall-2013/pages/unit-i/lecture-1/ | D11 finite sets/fractions | Reinforce sample spaces and event axioms before conditional reliability models | 45 min optional |
| Introduction to Derivatives / David Jerison, MIT 18.01SC | https://ocw.mit.edu/courses/18-01sc-single-variable-calculus-fall-2010/pages/1.-differentiation/part-a-definition-and-basic-rules/session-1-introduction-to-derivatives/ | D12 scalar algebra | Reinforce rate-of-change intuition and finite-difference derivation | 40 min optional |

These additions resolve the earlier vector/probability/calculus source-selection
gap. The introductory probability session is not claimed to cover every later
conditional-independence topic; the local chapter provides that essential teaching.

## Week 3 sources — retrieved 2026-11-17

Five additional public primary pages bring the selected set to 23. These are
supplementary references; the lessons contain original explanations and exercises.
Moving PyTorch documentation was inspected as reference, not installed or claimed
as a compatible dependency. No substantial external text or source was copied.

| Title / author | Verified URL / section | Prerequisites / lesson | Outcome | Estimate |
|---|---|---|---|---|
| Dividing datasets / Google | https://developers.google.com/machine-learning/crash-course/overfitting/dividing-datasets — train/validation/test | D12; D13/D17 | Preserve a meaningful evaluation boundary | 25 min |
| Linear regression loss / Google | https://developers.google.com/machine-learning/crash-course/linear-regression/loss — squared/absolute error | D13; D14 | Distinguish objective choice and residual magnitude | 25 min |
| Automatic differentiation / PyTorch | https://docs.pytorch.org/tutorials/beginner/basics/autogradqs_tutorial.html — graph and gradients | D15–16 | Compare local autograd semantics with a tensor library | 25 min |
| micrograd / Andrej Karpathy | https://github.com/karpathy/micrograd — project overview/source navigation | D16 | Compare scalar engine architecture after implementing independently | 30 min |
| Attention Is All You Need / Vaswani et al. | https://arxiv.org/abs/1706.03762 — abstract and paper metadata | D18; Week 4 preview | Locate the original transformer paper; abstract-only retrieval is not full paper verification | 10 min preview |

## Week 4 primary sources — retrieved 2026-11-17

Three additional selected URLs bring page-level verification to 26. No runtime
packages were introduced; PyTorch is reference reading, not an installed/pinned
implementation dependency. All essential mechanisms are authored locally.

| Title / author | URL / inspected section | Prerequisites / lesson | Outcome | Estimate |
|---|---|---|---|---|
| BPE / Hugging Face LLM Course | https://huggingface.co/learn/llm-course/en/chapter6/5 — training and encoding | D18; D19 | Compare ranked pair merging and production simplifications | 35 min |
| Attention Is All You Need / Vaswani et al. | https://arxiv.org/html/1706.03762v7 — architecture 3.1–3.5 and training | D19–24 | Verify Q/K/V, multi-head, FFN and positions against original paper | 90 min targeted across week |
| Scaled dot-product attention / PyTorch | https://docs.pytorch.org/docs/2.15/generated/torch.nn.functional.scaled_dot_product_attention.html — function and mask behavior | D21/D24 | Compare conventions with explicit causal prefix implementation | 20 min optional |

The original paper's full HTML was now retrieved, expanding the earlier abstract-
only inspection. Our decoder intentionally differs: pre-normalization, one block,
learned absolute positions and omitted optional bias/gain/dropout. No claim that
these are the internal choices of a proprietary model. Provider prompt caching,
pricing and compatibility remain pending official research in later phases.
