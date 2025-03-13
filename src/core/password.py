from base64 import b64encode
from hashlib import pbkdf2_hmac
from math import ceil, log2
from secrets import choice
from string import ascii_letters, digits

HASH_SPLITTER = "$"

SALT_CHARS = ascii_letters + digits

PBKDF2_ITERATIONS = 1_000_000
PBKDF2_ITERATIONS_STR = str(PBKDF2_ITERATIONS)
PBKDF2_SALT_LENGTH = ceil(128 / log2(len(SALT_CHARS)))


def get_password_hash(password: str) -> str:
    """Secure password hashing using the PBKDF2 algorithm."""

    salt = "".join(choice(SALT_CHARS) for _ in range(PBKDF2_SALT_LENGTH))
    hash_encoded = pbkdf2_hmac("sha256", password.encode(), salt.encode(), PBKDF2_ITERATIONS)
    password_hash = b64encode(hash_encoded).decode("ascii").strip()
    return HASH_SPLITTER.join((password_hash, salt, PBKDF2_ITERATIONS_STR))
