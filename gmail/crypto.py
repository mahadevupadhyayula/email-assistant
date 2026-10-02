import json
from typing import Any

from cryptography.fernet import Fernet, InvalidToken
from django.conf import settings


class CredentialEncryptionError(RuntimeError):
    """Raised when the local credential key is missing or invalid."""


def _fernet() -> Fernet:
    if not settings.GOOGLE_TOKEN_ENCRYPTION_KEY:
        raise CredentialEncryptionError("Token encryption is not configured.")
    try:
        return Fernet(settings.GOOGLE_TOKEN_ENCRYPTION_KEY.encode("ascii"))
    except (ValueError, UnicodeEncodeError) as exc:
        raise CredentialEncryptionError("Token encryption key is invalid.") from exc


def encrypt_credentials(credentials: dict[str, Any]) -> str:
    payload = json.dumps(credentials, separators=(",", ":"), sort_keys=True).encode()
    return _fernet().encrypt(payload).decode("ascii")


def decrypt_credentials(envelope: str) -> dict[str, Any]:
    try:
        payload = _fernet().decrypt(envelope.encode("ascii"))
        value = json.loads(payload)
    except (InvalidToken, ValueError, json.JSONDecodeError) as exc:
        raise CredentialEncryptionError("Stored credentials could not be decrypted.") from exc
    if not isinstance(value, dict):
        raise CredentialEncryptionError("Stored credentials have an invalid shape.")
    return value
