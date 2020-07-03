import json
import hashlib as hl


def hash_string_256(string):
    return hl.sha256(string).hexdigest()


def hash_block(block):
    # Dictionaries are unordered, so to ensure that the hashing algorithm always produces the same
    # hash for the same input, we set the short_keys method to True
    return hash_string_256(json.dumps(block, sort_keys=True).encode())