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
