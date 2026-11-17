# Week 6 review and remediation

Closed book, trace one source snapshot into revision-aware chunks, postings,
ranked IDs and cited answer. Derive one BM25 score, one cosine candidate-loss
example, one reciprocal-rank fusion and a graded nDCG. State exact conventions,
units and empty cases before executing tests.

Run the fixed [benchmark](../../scripts/benchmark_retrieval.py) and preserve every
query row. Explain why mean rr=.75 on this fixture can coexist with correct
abstention for every no-evidence query; do not change the denominator to make
it look perfect. Reproduce stale revision, fabricated quote and uncited extra
sentence failures. Show a real irrelevant quote can pass occurrence verification.

Take [weekly exam](../../assessments/weekly/week-06.md) and
[Phase 3 defense](../../assessments/phase-examinations/phase-03.md) before answers.
Remediate the first wrong boundary: span, statistic, vector compatibility,
candidate recall, rank convention, metric denominator or citation support.
Retest changed inputs. Recall after one week must include one arithmetic
mechanism and one provenance/security distinction.
