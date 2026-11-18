"""Reference: identity comes from configured credentials, not submitted text."""
import hmac


def authenticate(authorization, credential_to_owner):
    scheme, separator, supplied = (authorization or "").partition(" ")
    if not separator or scheme.lower() != "bearer" or not supplied:
        return None
    owner = None
    for credential, configured_owner in credential_to_owner.items():
        if hmac.compare_digest(supplied, credential):
            owner = configured_owner
    return owner


def lookup(owner, identifier, rows):
    row = rows.get(identifier)
    return row if row is not None and row.get("owner") == owner else None


def validate_submission(session_id, text, *, max_chars=4000):
    if not isinstance(session_id, str) or not 1 <= len(session_id) <= 128:
        raise ValueError("invalid session")
    if not isinstance(text, str) or not 1 <= len(text) <= max_chars:
        raise ValueError("invalid input")
    return session_id, text
