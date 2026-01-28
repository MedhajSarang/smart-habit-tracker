import hashlib

def make_hash(password):
    """
    Takes a plain password and returns a secure hash.
    Using SHA256 (Standard security).
    """
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hash(password, hashed_text):
    """
    Checks if a user's password matches the saved hash.
    """
    if make_hash(password) == hashed_text:
        return True
    return False