"""
Module de vérification de signatures avec Ed25519
"""

import hashlib
import base64
from pathlib import Path
from typing import Union, Optional, Tuple, Dict
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
import json


class SignatureVerifier:
    
    def __init__(self, public_key: VerifyKey):
        self.public_key = public_key

    def verify_file(self, file_path: Union[str, Path], 
                    signature_path: Optional[Union[str, Path]] = None) -> Tuple[bool, str]:
        file_path = Path(file_path)
        
        if not file_path.exists():
            return False, f"Fichier non trouvé: {file_path}"
        
        if signature_path is None:
            signature_path = file_path.with_suffix(file_path.suffix + '.sig')
        else:
            signature_path = Path(signature_path)
        
        if not signature_path.exists():
            return False, f"Signature non trouvée: {signature_path}"
        
        try:
            with open(signature_path, 'r') as f:
                manifest = json.load(f)
        except json.JSONDecodeError:
            return False, "Fichier de signature invalide"
        
        signature_b64 = manifest.get('signature')
        if not signature_b64:
            return False, "Signature manquante"
        
        with open(file_path, 'rb') as f:
            current_content = f.read()
        
        current_hash = hashlib.sha256(current_content).digest()
        
        try:
            signature_bytes = base64.b64decode(signature_b64)
            
            # CORRECTION: Vérifier la taille
            if len(signature_bytes) != 64:
                return False, f"Signature invalide (taille {len(signature_bytes)} bytes)"
            
            self.public_key.verify(current_hash, signature_bytes)
            return True, "✓ Signature VALIDE"
            
        except BadSignatureError:
            return False, "✗ Signature INVALIDE"
        except Exception as e:
            return False, f"Erreur: {str(e)}"
    
    def verify_update_package(self, package_path: Union[str, Path],
                              signature_path: Optional[Union[str, Path]] = None) -> bool:
        is_valid, message = self.verify_file(package_path, signature_path)
        print(message)
        return is_valid

    def batch_verify(self, directory: Union[str, Path]) -> Dict[str, bool]:
        directory = Path(directory)
        results = {}
        
        for sig_file in directory.glob("*.sig"):
            original_file = sig_file.with_suffix('')
            if original_file.exists():
                is_valid, message = self.verify_file(original_file, sig_file)
                results[str(original_file)] = is_valid
                print(f"{'✓' if is_valid else '✗'} {original_file.name}: {message}")
        
        return results