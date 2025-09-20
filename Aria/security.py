import os
import hashlib
from typing import Tuple


ALGORITHM = "pbkdf2_sha256"
ITERATIONS = 200_000
SALT_BYTES = 16


def _pbkdf2(password: str, salt: bytes, iterations: int) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)


def hash_password(password: str) -> str:
    salt = os.urandom(SALT_BYTES)
    dk = _pbkdf2(password, salt, ITERATIONS)
    return f"{ALGORITHM}${ITERATIONS}${salt.hex()}${dk.hex()}"


def _parse(stored: str) -> Tuple[str, int, bytes, bytes]:
    try:
        algo, it_str, salt_hex, hash_hex = stored.split("$")
        return algo, int(it_str), bytes.fromhex(salt_hex), bytes.fromhex(hash_hex)
    except Exception as exc:
        raise ValueError("Formato de hash inválido") from exc


def verify_password(stored: str, provided: str) -> bool:
    algo, iterations, salt, expected = _parse(stored)
    if algo != ALGORITHM:
        return False
    computed = _pbkdf2(provided, salt, iterations)
    return hashlib.compare_digest(computed, expected)

