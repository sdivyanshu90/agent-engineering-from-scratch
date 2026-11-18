# Hints

1. Validate the result container and the boolean `isError` before reading text. Do not turn `isError: true` into success by extracting its content.
2. Trim whitespace, lowercase ASCII, then apply a whole-string regular expression. Reject slashes, dots, and repeated separators.
3. Canonical JSON must have stable key order and separators. Identity belongs in the digest along with the revision; changing any field changes the binding.
4. Validate exact fields and types before comparing list uniqueness. Strings are iterable, so first insist on a list.
5. Hash bytes directly with SHA-256. Text encoding decisions belong to the caller.
6. Membership is an exact policy decision. Do not infer permissions from a name prefix or a tool description.
