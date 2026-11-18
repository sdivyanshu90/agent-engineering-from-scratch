"""D61 starter: never accept owner identity from the caller's body."""


def authenticate(authorization, credential_to_owner):
    """Return configured owner for a valid Bearer credential, otherwise None."""
    raise NotImplementedError


def lookup(owner, identifier, rows):
    """Return a row only when both its identifier and owner match."""
    raise NotImplementedError


def validate_submission(session_id, text, *, max_chars=4000):
    """Return normalized (session_id, text) or raise ValueError."""
    raise NotImplementedError
