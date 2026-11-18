# Week 10 labs — evaluate and secure agent systems

Complete one starter per day. The public checks are executable contracts, not
proof of production security. Run from the repository root:

```sh
python labs/week-10/checks.py --day 1
python labs/week-10/checks.py --day 1 --module /tmp/my_submission.py
```

1. `route_comparison.py`: aggregate equally specified route outcome records.
2. `intervals.py`: calculate Wilson intervals and identify the sample size.
3. `redaction.py`: export reviewed metadata while removing payload fields.
4. `fixture_integrity.py`: verify a frozen fixture against a supplied digest.
5. `calibration.py`: compare human supplied labels with model-like scored labels.
6. `boundary_audit.py`: assess exact runtime boundary outcomes, not attack strings.

The [hints](hints.md) reveal one conceptual step per problem. Full reference
implementations are in `solutions/labs/week-10/`.
