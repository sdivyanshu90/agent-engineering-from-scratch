# Concept dependencies

The machine-readable schedule is [build-progress.json](docs/build-progress.json).
Its conservative edges require the preceding lesson. This prevents unsupported
skips; finer concept edges will replace the chain as later chapters are audited.
Weeks 1–6 currently have authored instruction.

```mermaid
flowchart TD
  A[Execution and values D01] --> B[Conditions and loops D02]
  B --> C[Functions and collections D03]
  C --> D[Files and errors D04]
  D --> E[Objects and tests D05]
  E --> F[CLI integration and complexity D06]
  F --> G[HTTP and persistence W02]
  G --> H[Concurrency and recovery W02]
  C --> I[Vectors and derivatives W02]
  I --> J[Autograd and networks W03]
  J --> K[Attention and generation W04]
  H --> L[Model integration W05]
  K --> L
  L --> M[Retrieval and grounding W06]
  M --> N[Agent runtime W07]
  N --> O[Context and durability W08]
  O --> P[MCP and execution boundaries W09]
  P --> Q[Security and evaluation W10]
  Q --> R[Production operations W11]
  R --> S[ForgeAgent defense W12]
```

An arrow means the destination needs the source's demonstrated competence.
It does not imply every intermediate topic is already authored. A complete
concept-to-lesson coverage matrix is a planned deliverable; the current matrix
records only concepts actually taught.
