# Week 6 reference criteria

Daily five points correspond to concept/trace/independent code/debug/judgment;
require four including code. Weekly allocation is fixed20/30/20/20/10.

D31: window3/overlap1 on five lines yields spans1–3,3–5; preserve newlines.
Stride must be positive. Full-source SHA-256 revision changes all chunk identities
when any source text changes. Path/revision/span and authorization precede context.
Overlap repeats evidence and is not independent support or a model-token bound.

D32: tf counts occurrences in one chunk; df counts matching chunks. For two
length-two chunks agent-agent/tests-tests, IDF=ln2 and tf factor=4.4/3.2=1.375,
score≈.95308. Query terms are unique by this contract. Stable score/ID order,
no-postings behavior and empty corpus need explicit tests. Other engine variants
may have different absolute scores; score is not probability.

D33: q=[.01,1], near=[−.01,1] cosine≈.9998; far=[1,0]≈.01. Sign-bucket ANN
excludes near, so exact-top1 recall becomes zero. This is candidate loss, not
an embedding-quality experiment. TF-IDF and authored vectors are not pretrained
semantic models. Nonzero equal-width finite vectors are required; real encoder
versions/task preprocessing must match beyond shape.

D34: original unweighted RRF uses one-based r and 1/(60+r). A=[x,y],B=[y,z]
gives y≈.03252,x≈.01639,z≈.01613. Raw-score scaling cannot change fusion if
ranks stay fixed. Duplicate within-list IDs reject. Reranking cannot recover
an absent candidate; rewriting needs original intent/provenance and fixed labels.

D35: [b,x,a],grades a2,b1,k3 has precision2/3,recall1,rr1,DCG2.5,ideal
3+1/log2(3),nDCG≈.68853. Exponential gain is our declared convention; many libraries
use linear gain. Empty ideal returns0; duplicate IDs reject; fewer returned slots
do not change precision denominator. No-answer task correctness uses separate abstention.

D36: every citation refers to supplied selected current evidence, exact nonempty
quote and matching revision. Answer equals joined quotes or explicit abstention.
Extra paraphrase rejects under this narrow mechanical contract. A real irrelevant
quote can pass provenance; semantic relevance/source truth remain separate.
Always-abstain can have vacuous citation validity but fail useful-answer coverage.
FakeProvider quote selection is not live-model quality. No retrieved instruction
authorizes execution.

The visible benchmark has three answerable queries and one absent-evidence query;
mean reciprocal rank across all four is .75 under its fixed convention. Citation
validity and abstention correctness should both be reported separately. Do not
remove the no-answer row or edit relevance labels merely to improve reported scores.
