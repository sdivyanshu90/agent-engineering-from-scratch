import hashlib
def verify(raw_bytes,expected_hex):return hashlib.sha256(raw_bytes).hexdigest()==expected_hex
