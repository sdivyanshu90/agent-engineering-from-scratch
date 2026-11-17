# Reading official documentation productively

Use [the resource library](../RESOURCE_LIBRARY.md) after the corresponding
local explanation. Pick one behavior you need to verify, locate its named
section, write an expected example, run it, and record the result. Do not read
an entire reference manual linearly before attempting a lab.

Documentation tells you an interface's contract; it does not prove your program
uses that contract correctly. A type annotation does not imply runtime checking.
A successful HTTP request does not establish semantic correctness. A protocol
version label does not mean two implementations interoperate. Keep small tests
alongside the assumptions your design depends on.

For moving sources record retrieval date and version. Keep quoted excerpts short
and attribute them. Author your own conceptual explanation and test fixture
rather than reproducing a copyrighted chapter. The current verified set is
listed in [the ledger](../docs/resource-verification.md); future source selections
remain pending until their lessons are authored.
