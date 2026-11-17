# Resource library

Core teaching is local; external reading supplements it. The current verified
set supports Weeks 1–2. “Verified” means content was retrieved and inspected, not
that it will never change. See [resource verification](docs/resource-verification.md)
for retrieval dates, access model, prerequisites, outcomes, and estimates.

| Objective | Selected primary reference | Local lesson |
|---|---|---|
| Values and text | [Python introduction](https://docs.python.org/3.12/tutorial/introduction.html) | [D01](curriculum/week-01/day-01/README.md) |
| Conditions, iteration, functions | [Python control flow](https://docs.python.org/3.12/tutorial/controlflow.html) | [D02](curriculum/week-01/day-02/README.md), [D03](curriculum/week-01/day-03/README.md) |
| Collections | [Python data structures](https://docs.python.org/3.12/tutorial/datastructures.html) | [D03](curriculum/week-01/day-03/README.md) |
| Encodings and reads | [Python input/output](https://docs.python.org/3.12/tutorial/inputoutput.html) | [D04](curriculum/week-01/day-04/README.md) |
| Failure propagation | [Python exceptions](https://docs.python.org/3.12/tutorial/errors.html) | [D04](curriculum/week-01/day-04/README.md) |
| Objects and scope | [Python classes](https://docs.python.org/3.12/tutorial/classes.html) | [D05](curriculum/week-01/day-05/README.md) |
| Automated tests | [Python unittest](https://docs.python.org/3.12/library/unittest.html) | [D05](curriculum/week-01/day-05/README.md), [D06](curriculum/week-01/day-06/README.md) |
| Environment workflow | [uv projects](https://docs.astral.sh/uv/guides/projects/) | [Setup](START_HERE.md) |

[Documentation guide](resources/documentation.md) explains how to use these
sources. Additional books/courses/papers lists are deliberately not published
until selected sources have been researched for authored chapters. This avoids
padding the library with redundant or unchecked links. Research still needed:
CS50P, Google ML Crash Course, Karpathy, 3Blue1Brown, Hugging Face, PyTorch,
provider APIs, Anthropic engineering, Qdrant, MCP, Agent Skills, A2A, public
Codex source, OWASP, pytest, FastAPI, Docker, and OpenTelemetry. These names
are a research queue, not verified coverage or compatibility claims.

## Week 2 additions

[HTTP semantics RFC](https://www.rfc-editor.org/rfc/rfc9110.html),
[Python JSON](https://docs.python.org/3.12/library/json.html),
[SQLite](https://docs.python.org/3.12/library/sqlite3.html),
[async tasks](https://docs.python.org/3.12/library/asyncio-task.html),
[async streams](https://docs.python.org/3.12/library/asyncio-stream.html),
[Google gradient descent](https://developers.google.com/machine-learning/crash-course/linear-regression/gradient-descent),
and [Google sigmoid](https://developers.google.com/machine-learning/crash-course/logistic-regression/sigmoid-function)
add seven selected verified primary pages (fifteen total). Core vector/probability
and calculus instruction is authored locally; targeted MIT vector/probability/calculus
supplements are recorded below.

## Mathematics reinforcement

[MIT geometry of linear equations](https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/pages/ax-b-and-the-four-subspaces/the-geometry-of-linear-equations/),
[MIT probability models and axioms](https://ocw.mit.edu/courses/6-041sc-probabilistic-systems-analysis-and-applied-probability-fall-2013/pages/unit-i/lecture-1/),
and [MIT introduction to derivatives](https://ocw.mit.edu/courses/18-01sc-single-variable-calculus-fall-2010/pages/1.-differentiation/part-a-definition-and-basic-rules/session-1-introduction-to-derivatives/)
are optional targeted supplements for Days 11–12. Eighteen selected primary
source pages have now been retrieved; session-page verification does not mean
all associated video or PDF content has been reviewed.

## Week 3 targeted reading

The [verification ledger](docs/resource-verification.md) records five additional
primary pages: Google dataset/loss instruction, PyTorch autograd, Karpathy's
micrograd, and the original transformer paper's abstract/metadata. Read these
after the local mechanisms. Twenty-three selected pages have been retrieved;
the paper's full text and moving API compatibility require separate verification.

## Week 4 internals

[Hugging Face BPE](https://huggingface.co/learn/llm-course/en/chapter6/5),
[full original transformer paper](https://arxiv.org/html/1706.03762v7), and
[versioned PyTorch attention reference](https://docs.pytorch.org/docs/2.15/generated/torch.nn.functional.scaled_dot_product_attention.html)
supplement the six original transformer chapters. Twenty-six selected page URLs
are verified; the local implementation needs no external training framework.

## Week 5 application boundaries

Official [Responses](https://developers.openai.com/api/reference/resources/responses/methods/create),
[structured-output](https://developers.openai.com/api/docs/guides/structured-outputs)
and [streaming](https://developers.openai.com/api/docs/guides/streaming-responses)
references accompany local implementation. JSON Schema and pinned Pydantic records
are in the ledger. Thirty-two selected primary URLs have been inspected; no
live-model evaluation or current pricing claim follows from documentation retrieval.

## Week 6 retrieval and grounding

The ledger adds Elastic/Lucene scoring references, Qdrant indexing/hybrid pages,
the original RRF paper and scikit-learn nDCG documentation (38 selected URLs total).
Failed Stanford/older-version retrievals are disclosed. Essential instruction,
metrics, citations and fixed benchmark are implemented locally. No installed
vector database or pretrained semantic quality is implied by these references.
