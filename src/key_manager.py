# Gestionnaire de clés cryptographiques Ed25519 Utilise la bibliothèque PyNaCl pour la génération et la gestion des clés


import os
import base64
from pathlib import Path
from nacl.signing import SigningKey, VerifyKey
from nacl.encoding import RawEncoder, Base64Encoder
import json
from typing import Tuple, Dict, Optional

class KeyManager:
    
# Gère la génération, le chargement et la sauvegarde des clés Ed25519
    
    
    def __init__(self, key_dir: str = "keys"):
        """
        Initialise le gestionnaire de clés
        
        Args:
            key_dir: Dossier où stocker les fichiers de clés
        """
        self.key_dir = Path(key_dir)
        self.key_dir.mkdir(exist_ok=True)

# Génère une nouvelle paire de clés Ed25519
        
    def generate_keypair(self, name: str = "default") -> Tuple[SigningKey, VerifyKey]:
        
        # Génération de la clé privée (qui contient aussi la clé publique)
        private_key = SigningKey.generate()
        public_key = private_key.verify_key
        
        # Sauvegarde des clés
        self._save_keys(private_key, public_key, name)
        
        return private_key, public_key
    
# Sauvegarde les clés dans des fichiers séparés en utilisant le format Base64 pour faciliter le stockage et l'échange
    
    def _save_keys(self, private_key: SigningKey, public_key: VerifyKey, name: str):

        # Sauvegarde clé privée (encodée en Base64)
        priv_key_path = self.key_dir / f"{name}_private.key"
        with open(priv_key_path, 'w') as f:
            f.write(base64.b64encode(private_key.encode()).decode())
        
        # Sauvegarde clé publique
        pub_key_path = self.key_dir / f"{name}_public.key"
        with open(pub_key_path, 'w') as f:
            f.write(base64.b64encode(public_key.encode()).decode())
        
        # Métadonnées
        metadata = {
            "name": name,
            "algorithm": "Ed25519",
            "created_at": str(Path(priv_key_path).stat().st_ctime)
        }
        metadata_path = self.key_dir / f"{name}_metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
            
        # Ajuster les permissions (lecture seule pour la clé privée)
        os.chmod(priv_key_path, 0o600)

# Charge une clé privée depuis un fichier
        
    def load_private_key(self, name: str = "default") -> SigningKey:
        
        priv_key_path = self.key_dir / f"{name}_private.key"
        
        if not priv_key_path.exists():
            raise FileNotFoundError(f"Clé privée non trouvée: {priv_key_path}")
        
        with open(priv_key_path, 'r') as f:
            key_data = base64.b64decode(f.read().strip())
        
        return SigningKey(key_data, encoder=RawEncoder)
    


 #  Charge une clé publique depuis un fichier 
    
    def load_public_key(self, name: str = "default") -> VerifyKey:
        
        pub_key_path = self.key_dir / f"{name}_public.key"
        
        if not pub_key_path.exists():
            raise FileNotFoundError(f"Clé publique non trouvée: {pub_key_path}")
        
        with open(pub_key_path, 'r') as f:
            key_data = base64.b64decode(f.read().strip())
        
        return VerifyKey(key_data, encoder=RawEncoder)

    
 # Exporte la clé publique au format Base64 pour distribution
    def export_public_key(self, name: str = "default") -> str:
        pub_key = self.load_public_key(name)
        return base64.b64encode(pub_key.encode()).decode()
    
        
# Liste toutes les paires de clés disponibles  
    def list_keypairs(self) -> Dict[str, Dict]:
        
        keypairs = {}
        for metadata_file in self.key_dir.glob("*_metadata.json"):
            with open(metadata_file, 'r') as f:
                metadata = json.load(f)
                keypairs[metadata['name']] = metadata
        return keypairs