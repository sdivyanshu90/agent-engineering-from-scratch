# Technical standards

Reference functions document input/output and failure semantics. Pure logic is
separate from filesystem or network effects. Use deterministic fixtures, explicit
encodings, stable sort order, and temporary directories for tests. Never require
paid inference for normal checks. Introduce a framework only after its central
abstraction is implemented or traced manually.

Python default: 3.12. Supported: 3.12 through 3.14. No third-party dependencies
at this checkpoint. The uv lock records an empty dependency graph; the Python
patch version depends on the available security release. Run from the repository
root. `python` commands below mean the selected virtual-environment interpreter.

Test claims require executed commands and recorded outcomes. CI separates
checkpoint integrity from final completeness: the checkpoint can pass while the
full build remains incomplete. `validate_curriculum.py --require-complete` must
fail until all planned deliverables exist and are validated.

Mermaid diagrams are maintained as Markdown code blocks. External resources
are supplements; all essential explanations must be locally authored. URLs
have verification dates and retrieval limitations. A successful HTTP response
is not evidence of a compatible SDK implementation. Reverify moving standards
before adopting them.
