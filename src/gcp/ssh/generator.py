import hashlib
import os
from dataclasses import dataclass

from cryptography.hazmat.backends import default_backend as crypto_default_backend
from cryptography.hazmat.primitives import serialization as crypto_serialization, serialization
from cryptography.hazmat.primitives.asymmetric import rsa


@dataclass
class KeyPair:
    private_key: str
    public_key: str
    passphrase: str
    fingerprint: str


class Generator:
    def generate_random_passphrase(self) -> str:
        stream = os.popen('gpg --gen-random --armor 1 24')
        output = stream.read()

        return output.strip()

    def calculate_fingerprint(self, message: str) -> str:
        sha256 = hashlib.sha256()
        sha256.update(message.encode())

        return sha256.hexdigest()

    def generate_key_pair(self) -> KeyPair:
        key = rsa.generate_private_key(
            backend=crypto_default_backend(),
            public_exponent=65537,
            key_size=4096
        )
        passphrase = self.generate_random_passphrase()
        public_key = key.public_key().public_bytes(
            crypto_serialization.Encoding.OpenSSH,
            crypto_serialization.PublicFormat.OpenSSH
        )
        private_key = key.private_bytes(
            crypto_serialization.Encoding.PEM,
            crypto_serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.BestAvailableEncryption(passphrase.encode()))
        key_pair = KeyPair(
            private_key=private_key.decode('utf-8'),
            public_key=public_key.decode('utf-8'),
            passphrase=passphrase,
            fingerprint=self.calculate_fingerprint(public_key.decode('utf-8'))
        )

        return key_pair
