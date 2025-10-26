import base64
import hashlib
from typing import Dict


class KawaiiRyugagotokuClass:
    """
    Ultra-simple XOR-based obfuscation.
    Faster and lighter than Fernet, but less secure (fine for obfuscation).
    """

    @staticmethod
    def _get_key() -> bytes:
        """Generate obfuscation key from code constants"""
        # Hidden in plain sight - looks like random hex strings
        parts = [
            "a7f9d3e9b2c4",
            "6e5d8f2a8c1b",
            "3b7e1f9d2a6c",
        ]
        combined = ''.join(parts)
        # Create repeating key
        return hashlib.sha256(combined.encode()).digest()

    @staticmethod
    def decrypt(obfuscated: str) -> str:
        """XOR-based de-obfuscation (XOR is symmetric)"""
        key = KawaiiRyugagotokuClass._get_key()
        obfuscated_bytes = base64.b64decode(obfuscated.encode('utf-8'))

        # XOR each byte with corresponding key byte
        credential = bytearray()
        for i, byte in enumerate(obfuscated_bytes):
            credential.append(byte ^ key[i % len(key)])

        return credential.decode('utf-8')

    @staticmethod
    def descrypt_dict(input: Dict):
        output = {}
        for key, value in input.items():
            output[key] = KawaiiRyugagotokuClass.decrypt(value)
        return output
