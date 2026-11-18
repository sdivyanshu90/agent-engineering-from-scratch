# Week 12 lab reference reasoning

D67 uses lexical set overlap and deterministic ordering. It reports a score and
first matching line, not semantic relevance. D68 requires a chronological
proposal/approval/apply/test sequence, matching proposal identity and review
digest, and the same post-apply revision at test time. D69 canonicalizes the
review tuple; this binds fields but does not authenticate a reviewer. D70 fixes
the argv and delegates to the supplied isolation backend. An absent backend
raises through `TestExecutor`; this is the intended safe default. D71 recovers
the latest full snapshot event after a checkpoint revision, which covers the
append-before-checkpoint crash interval. D72 preserves each fixed case in the
denominator and reports split-specific results. None of these contracts proves
agent generalization, backend isolation, or reviewer intent. Those require
separate system evidence.
