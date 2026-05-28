"""
Module de signature de fichiers avec Ed25519
"""

import hashlib
import base64
from pathlib import Path
from typing import Union, Optional
from nacl.signing import SigningKey
import json
from datetime import datetime

class FileSigner:
    """Signe des fichiers avec une clé Ed25519"""

    def __init__(self, private_key: SigningKey):
        self.private_key = private_key

    def sign_file(self, file_path: Union[str, Path], 
                  signature_path: Optional[Union[str, Path]] = None) -> str:
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Fichier non trouvé: {file_path}")
        
        with open(file_path, 'rb') as f:
            file_content = f.read()

        file_hash = hashlib.sha256(file_content).digest()

        # CORRECTION IMPORTANTE
        signed = self.private_key.sign(file_hash)
        signature_bytes = signed.signature  # Signature pure de 64 bytes
        signature_b64 = base64.b64encode(signature_bytes).decode()

        if signature_path is None:
            signature_path = file_path.with_suffix(file_path.suffix + '.sig')
        else:
            signature_path = Path(signature_path)
        
        manifest = {
            "file": str(file_path),
            "filename": file_path.name,
            "signature": signature_b64,
            "algorithm": "Ed25519",
            "hash_algorithm": "SHA256",
            "timestamp": datetime.now().isoformat(),
            "file_size": file_path.stat().st_size
        }
        
        with open(signature_path, 'w') as f:
            json.dump(manifest, f, indent=2)
        
        print(f"Fichier signé: {file_path}")
        print(f"Signature sauvegardée: {signature_path}")
        
        return signature_b64

    def sign_bytes(self, data: bytes) -> str:
        file_hash = hashlib.sha256(data).digest()
        signed = self.private_key.sign(file_hash)
        return base64.b64encode(signed.signature).decode()