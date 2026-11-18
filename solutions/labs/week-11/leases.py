"""Reference: immutable-copy queue transitions with a fencing token."""
from copy import deepcopy


def claim(rows, now, lease_seconds, token):
    if lease_seconds <= 0 or not token:
        raise ValueError("positive lease and token required")
    candidates = [row for row in rows.values()
                  if row["state"] == "queued" or
                  (row["state"] == "running" and row["lease_until"] < now)]
    if not candidates:
        return None
    selected = min(candidates, key=lambda row: (row["created_at"], row["job_id"]))
    updated = deepcopy(selected)
    updated.update(state="running", attempts=updated["attempts"] + 1,
                   lease_until=now + lease_seconds, lease_token=token)
    rows[updated["job_id"]] = updated
    return deepcopy(updated)


def finish(rows, job_id, token, result):
    row = rows.get(job_id)
    if row is None or row["state"] != "running" or row["lease_token"] != token:
        return False
    row.update(state="succeeded", result=result, lease_until=None, lease_token=None)
    return True
