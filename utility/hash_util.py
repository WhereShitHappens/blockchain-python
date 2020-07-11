import json
import hashlib as hl

# We control what is exported with '__all__'
# __all__ = ['hash_string_256', 'hash_block']

def hash_string_256(string):
    """
    Arguments:
        :param string: The string which should be hashed
    """
    return hl.sha256(string).hexdigest()


def hash_block(block):
    """Hashes a block and returns a string representation of it.

    Arguments:
        :block: The block that should be hashed.
    """
    hashable_block = block.__dict__.copy()
    hashable_block['transactions'] = [tx.to_ordered_dict() for tx in hashable_block['transactions']]
    print('Hashable block: ', hashable_block)
    # Dictionaries are unordered, so to ensure that the hashing algorithm always produces the same
    # hash for the same input, we set the short_keys method to True
    return hash_string_256(json.dumps(hashable_block, sort_keys=True).encode())