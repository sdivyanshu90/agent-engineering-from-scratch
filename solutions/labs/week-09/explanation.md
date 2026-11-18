# Week 9 lab solutions

`tasks.py` contains the six reference functions. The checker uses deterministic input and no network. `parse_tool_result` validates the envelope before trusting the content; a tool-level error is not treated as text success. Skill identifiers use a deliberately small ASCII subset. Approval binding canonicalizes JSON before hashing so dictionary key order does not change the result. The manifest example requires exact keys and rejects duplicate capability names. Content hashing accepts bytes to make encoding explicit. Tool authorization is exact allowlist membership.

These six helpers do not replace the actual MCP subprocess tests or workspace security tests. Run those separately with `python3 -m unittest tests.integration.test_mcp tests.security.test_policy -v`. A passing public check is not a claim of full MCP, Agent Skills, or A2A conformance.
