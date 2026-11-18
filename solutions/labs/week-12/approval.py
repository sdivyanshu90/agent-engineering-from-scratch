import hashlib
import json

def review_digest(path,before_sha256,after_sha256):
    if not all(isinstance(x,str) and x for x in (path,before_sha256,after_sha256)):
        raise ValueError("nonempty binding fields required")
    payload=json.dumps({"path":path,"before":before_sha256,"after":after_sha256},
        sort_keys=True,separators=(",",":"),ensure_ascii=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()
