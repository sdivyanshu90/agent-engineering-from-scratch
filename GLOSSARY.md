# Glossary of taught concepts

Only taught terms are included; later agent terminology will be added alongside
its actual instruction rather than used as an unexplained prerequisite.

| Term | Beginner definition | Introduction |
|---|---|---|
| Interpreter | Program that executes Python instructions | [D01](curriculum/week-01/day-01/README.md) |
| Process | Running program with memory and OS-managed resources | [D01](curriculum/week-01/day-01/README.md) |
| Expression | Code that computes a value | [D01](curriculum/week-01/day-01/README.md) |
| Statement | Instruction such as binding a name or choosing a branch | [D01](curriculum/week-01/day-01/README.md) |
| Type | Kind of value determining supported operations | [D01](curriculum/week-01/day-01/README.md) |
| Binding | Association between a name and an object | [D01](curriculum/week-01/day-01/README.md) |
| Unicode code point | Integer-assigned unit represented in Python text; not always a whole visible character | [D01](curriculum/week-01/day-01/README.md) |
| Boolean | True/false value used for decisions | [D02](curriculum/week-01/day-02/README.md) |
| Mutation | Changing an existing object's contents | [D02](curriculum/week-01/day-02/README.md) |
| Rebinding | Making a name refer to a different value | [D02](curriculum/week-01/day-02/README.md) |
| Normalization | Explicit policy turning equivalent-looking inputs into a common representation | [D02](curriculum/week-01/day-02/README.md) |
| Invariant | Claim preserved through each iteration or transition | [D02](curriculum/week-01/day-02/README.md) |
| Function | Reusable behavior taking arguments and returning a value | [D03](curriculum/week-01/day-03/README.md) |
| Scope | Region/rules determining how names are resolved | [D03](curriculum/week-01/day-03/README.md) |
| Dictionary | Mapping from hashable keys to values | [D03](curriculum/week-01/day-03/README.md) |
| Set | Collection of unique hashable members | [D03](curriculum/week-01/day-03/README.md) |
| Tuple | Immutable sequence whose contained objects may themselves be mutable | [D03](curriculum/week-01/day-03/README.md) |
| Encoding | Agreement mapping text to bytes and back | [D04](curriculum/week-01/day-04/README.md) |
| Exception | Signal that an operation failed to produce its ordinary result | [D04](curriculum/week-01/day-04/README.md) |
| Module | Importable Python source unit | [D04](curriculum/week-01/day-04/README.md) |
| Package | Grouping of modules under a shared import name | [D04](curriculum/week-01/day-04/README.md) |
| Class / instance | Object description / one object constructed from it | [D05](curriculum/week-01/day-05/README.md) |
| Dataclass | Class transformed to supply common data-record behavior | [D05](curriculum/week-01/day-05/README.md) |
| Type hint | Description for readers/tools of an expected type; not ordinary runtime validation | [D05](curriculum/week-01/day-05/README.md) |
| Fixture | Known test input and setup | [D05](curriculum/week-01/day-05/README.md) |
| Regression test | Test retained to detect a previous defect returning | [D05](curriculum/week-01/day-05/README.md) |
| Complexity | How computational work or space grows with input size | [D06](curriculum/week-01/day-06/README.md) |
| CLI | Interface using command arguments and process outputs | [D06](curriculum/week-01/day-06/README.md) |
| JSON | Text interchange format with explicitly defined values and punctuation | [D06](curriculum/week-01/day-06/README.md) |
| Stdout / stderr | Normal process output / diagnostic output channels | [D06](curriculum/week-01/day-06/README.md) |
| Exit status | Small process-level success/failure indicator | [D06](curriculum/week-01/day-06/README.md) |
| Commit | Git snapshot of selected tracked changes and a message | [D06](curriculum/week-01/day-06/README.md) |
| Sandbox | Execution boundary restricting capabilities; stronger than filename filtering | [D06](curriculum/week-01/day-06/README.md) |

## Week 2 additions

| Term | Beginner definition | Introduction |
|---|---|---|
| Client / server | Process requesting work / process accepting requests | [D07](curriculum/week-02/day-01/README.md) |
| IP address / port | Network destination / selected endpoint there | [D07](curriculum/week-02/day-01/README.md) |
| HTTP | Protocol defining requests, representations, methods, and response statuses | [D07](curriculum/week-02/day-01/README.md) |
| Schema | Rules for a value's structure and field types | [D07](curriculum/week-02/day-01/README.md) |
| Authentication | Establishing the requesting identity | [D07](curriculum/week-02/day-01/README.md) |
| Authorization | Deciding what that identity may do to a resource | [D07](curriculum/week-02/day-01/README.md) |
| Primary key | Column(s) uniquely identifying a row | [D08](curriculum/week-02/day-02/README.md) |
| Transaction | State-change bundle committed together or rolled back | [D08](curriculum/week-02/day-02/README.md) |
| Parameterized SQL | Keeping supplied values separate from SQL structure | [D08](curriculum/week-02/day-02/README.md) |
| Idempotency | Repeating the same operation has the same intended state effect | [D08](curriculum/week-02/day-02/README.md) |
| Concurrency | Overlapping progress among tasks | [D09](curriculum/week-02/day-03/README.md) |
| Parallelism | Simultaneous execution | [D09](curriculum/week-02/day-03/README.md) |
| Coroutine / task | Async computation / its scheduled execution object | [D09](curriculum/week-02/day-03/README.md) |
| Event loop | Scheduler coordinating ready work and I/O waits | [D09](curriculum/week-02/day-03/README.md) |
| Cancellation | Cooperative request for work to stop, not automatic undo | [D09](curriculum/week-02/day-03/README.md) |
| Timeout / deadline | Limit on one wait / end time for a larger task | [D10](curriculum/week-02/day-04/README.md) |
| Backoff | Delay between eligible retries | [D10](curriculum/week-02/day-04/README.md) |
| Fault injection | Deliberately changing a dependency outcome to test recovery | [D10](curriculum/week-02/day-04/README.md) |
| Vector / matrix | Ordered coordinates / rectangular numerical table | [D11](curriculum/week-02/day-05/README.md) |
| Dot product | Sum of matching coordinate products | [D11](curriculum/week-02/day-05/README.md) |
| Norm | Length measure of a vector | [D11](curriculum/week-02/day-05/README.md) |
| Cosine similarity | Dot product normalized by lengths; undefined for zero direction | [D11](curriculum/week-02/day-05/README.md) |
| Conditional probability | Probability within the outcomes of a specified event | [D11](curriculum/week-02/day-05/README.md) |
| Independence | Joint event probability factors into individual probabilities | [D11](curriculum/week-02/day-05/README.md) |
| Derivative | Local rate of output change with input change | [D12](curriculum/week-02/day-06/README.md) |
| Chain rule | Multiplying local rates through function composition | [D12](curriculum/week-02/day-06/README.md) |
| Gradient | Vector of partial derivatives | [D12](curriculum/week-02/day-06/README.md) |
| Gradient descent | Parameter update subtracting learning rate times gradient | [D12](curriculum/week-02/day-06/README.md) |
| Logarithm | Inverse of an exponential on positive values | [D12](curriculum/week-02/day-06/README.md) |
| Softmax | Exponentiate scores and normalize by their sum | [D12](curriculum/week-02/day-06/README.md) |

## Week 3 additions

| Term | Definition | Introduction |
|---|---|---|
| Feature / label | Observed input / target used to assess or train a prediction | [D13](curriculum/week-03/day-01/README.md) |
| Parameter | Stored adjustable coefficient selected by training | [D13](curriculum/week-03/day-01/README.md) |
| Training / inference | Selecting parameters / applying selected parameters | [D13](curriculum/week-03/day-01/README.md) |
| Leakage | Evaluation information influencing fitting or selection improperly | [D13](curriculum/week-03/day-01/README.md) |
| Residual | Prediction minus target | [D14](curriculum/week-03/day-02/README.md) |
| Activation | Computed intermediate value; also the nonlinear mapping producing one | [D15](curriculum/week-03/day-03/README.md) |
| Computational graph | Executed value dependencies annotated with local operations | [D16](curriculum/week-03/day-04/README.md) |
| Backpropagation | Reverse chain-rule accumulation through an executed graph | [D16](curriculum/week-03/day-04/README.md) |
| Regularization | Objective/design preference constraining ways a model fits data | [D17](curriculum/week-03/day-05/README.md) |
| Bigram | Adjacent symbol pair, used here for one-character conditional prediction | [D18](curriculum/week-03/day-06/README.md) |
| Perplexity | Exponential mean negative log probability under a stated prediction unit | [D18](curriculum/week-03/day-06/README.md) |

## Week 4 additions

| Term | Definition | Introduction |
|---|---|---|
| Model token | Unit from a specific tokenizer, not necessarily a word | [D19](curriculum/week-04/day-01/README.md) |
| Embedding | Learned numerical row selected by a compatible token ID | [D19](curriculum/week-04/day-01/README.md) |
| Q/K/V | Learned comparison query/key and weighted payload vectors | [D20](curriculum/week-04/day-02/README.md) |
| Causal mask | Eligibility constraint excluding future positions | [D21](curriculum/week-04/day-03/README.md) |
| Attention head | One projected subspace's comparison-and-mixing operation | [D21](curriculum/week-04/day-03/README.md) |
| Residual | Input carried forward by adding a computed correction | [D22](curriculum/week-04/day-04/README.md) |
| Layer normalization | Per-token recentering/rescaling across feature coordinates | [D22](curriculum/week-04/day-04/README.md) |
| Cross-entropy | Negative log probability assigned to the labeled category | [D23](curriculum/week-04/day-05/README.md) |
| Teacher forcing | Training using known correct prior symbols under causal constraints | [D23](curriculum/week-04/day-05/README.md) |
| KV cache | Sequence/model-specific stored attention keys and values | [D24](curriculum/week-04/day-06/README.md) |
| Nucleus sampling | Keeping a leading probability prefix reaching a declared mass | [D24](curriculum/week-04/day-06/README.md) |

## Weeks 5–6 additions

| Term | Definition | Introduction |
|---|---|---|
| Provider adapter | Application-owned translation to a model interface | [D25](curriculum/week-05/day-01/README.md) |
| Prompt version | Explicit identity for an instruction recipe | [D26](curriculum/week-05/day-02/README.md) |
| JSON Schema | Structural/value rules for JSON documents; not factual verification | [D27](curriculum/week-05/day-03/README.md) |
| Stream delta | Provisional output fragment; not a completed application value | [D28](curriculum/week-05/day-04/README.md) |
| Rate admission | Policy deciding when a request may start | [D29](curriculum/week-05/day-05/README.md) |
| Cost per success | Total accounted attempt cost divided by successful tasks | [D30](curriculum/week-05/day-06/README.md) |
| Chunk provenance | Association of passage text with source revision and span | [D31](curriculum/week-06/day-01/README.md) |
| Inverted index | Term-to-matching-evidence lookup with statistics | [D32](curriculum/week-06/day-02/README.md) |
| ANN recall | Coverage of exact-neighbor results by approximate candidates | [D33](curriculum/week-06/day-03/README.md) |
| RRF | Ranking combination using reciprocal rank contributions | [D34](curriculum/week-06/day-04/README.md) |
| nDCG | Discounted graded relevance divided by ideal ordering under stated gain | [D35](curriculum/week-06/day-05/README.md) |
| Abstention | Explicitly declining an answer when the evidence/policy cannot support one | [D36](curriculum/week-06/day-06/README.md) |

## Weeks 7–12

| Term | Definition | Introduction |
|---|---|---|
| Agent harness | Host code that runs the model, tracks state and limits, and dispatches tools | [D37](curriculum/week-07/day-01/README.md) |
| Closed schema | Argument shape that admits only the stated fields | [D38](curriculum/week-07/day-02/README.md) |
| Observation | Host-produced record returned after a tool attempt | [D39](curriculum/week-07/day-03/README.md) |
| DAG | Directed graph with dependencies that cannot loop back to themselves | [D40](curriculum/week-07/day-04/README.md) |
| Compaction | Replacing a subset of context with a smaller, lossy representation | [D46](curriculum/week-08/day-04/README.md) |
| Checkpoint | A saved execution state associated with a point in the event history | [D47](curriculum/week-08/day-05/README.md) |
| Reconciliation | Checking external state before deciding the outcome of an uncertain operation | [D48](curriculum/week-08/day-06/README.md) |
| MCP | A protocol for connecting a host to tool and context servers | [D49](curriculum/week-09/day-01/README.md) |
| Skill | A packaged set of instructions and optional resources selected by the host | [D52](curriculum/week-09/day-04/README.md) |
| Agent Card | An A2A discovery document describing an agent and its capabilities | [D53](curriculum/week-09/day-05/README.md) |
| Trajectory | Ordered record of model decisions, tool attempts, and state transitions | [D57](curriculum/week-10/day-03/README.md) |
| Indirect prompt injection | An instruction embedded in retrieved input or tool output | [D58](curriculum/week-10/day-04/README.md) |
| Lease | Time-bounded claim on work that can be reassigned after expiry | [D63](curriculum/week-11/day-03/README.md) |
| Fencing token | A claim identifier used to reject writes from a superseded worker | [D63](curriculum/week-11/day-03/README.md) |
| Span | Timed operation inside a trace with associated attributes | [D64](curriculum/week-11/day-04/README.md) |
| Approval binding | Relation tying human authorization to one exact action and source revision | [D69](curriculum/week-12/day-03/README.md) |
| Namespace | Kernel boundary giving a process a separate view of a system resource | [D70](curriculum/week-12/day-04/README.md) |
