"""
Package de signature cryptographique pour mises à jour applicatives
Utilise Ed25519 via PyNaCl
"""

__version__ = "1.0.0"
__author__ = "Votre Nom"
__license__ = "MIT"

from .key_manager import KeyManager
from .signer import FileSigner
from .verifier import SignatureVerifier
from .update_policy import UpdatePolicy
from .attack_simulator import AttackSimulator

__all__ = [
    'KeyManager',
    'FileSigner',
    'SignatureVerifier',
    'UpdatePolicy',
    'AttackSimulator'
]