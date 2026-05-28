# Simulateur d'attaques pour tester la robustesse du système


import os
import random
import shutil
from pathlib import Path
from typing import Union, List, Dict
import hashlib

class AttackSimulator:
    
    # Simule différents types d'attaques sur les fichiers signés
    
    
    def __init__(self, verifier):
        
        # Initialise le simulateur d'attaques
        self.verifier = verifier
        self.attack_results = []
        
    def simulate_file_modification(self, file_path: Union[str, Path]) -> Dict:
        
        # Simule une attaque par modification directe du fichier
        file_path = Path(file_path)
        
        if not file_path.exists():
            return {"success": False, "error": "Fichier non trouvé"}
        
        # Sauvegarder le contenu original
        with open(file_path, 'rb') as f:
            original_content = f.read()
        
        # Modifier le fichier (ajouter des bytes aléatoires)
        with open(file_path, 'ab') as f:
            random_bytes = os.urandom(16)
            f.write(random_bytes)
        
        # Vérifier si la détection fonctionne
        is_valid, message = self.verifier.verify_file(file_path)
        
        # Restaurer le fichier original
        with open(file_path, 'wb') as f:
            f.write(original_content)
        
        result = {
            "attack_type": "file_modification",
            "file": str(file_path),
            "detected": not is_valid,
            "message": message,
            "success": True
        }
        
        self.attack_results.append(result)
        return result
    
    def simulate_signature_replacement(self, file_path: Union[str, Path],target_signature_path: Union[str, Path]) -> Dict:
        
        # Simule une attaque par remplacement de signature (fausse signature)
        file_path = Path(file_path)
        target_signature_path = Path(target_signature_path)
        
        if not target_signature_path.exists():
            return {"success": False, "error": "Signature cible non trouvée"}
        
        # Créer une fausse signature
        fake_signature = self._create_fake_signature(file_path)
        
        # Sauvegarder la signature originale
        with open(target_signature_path, 'r') as f:
            original_signature = f.read()
        
        # Remplacer par la fausse signature
        with open(target_signature_path, 'w') as f:
            f.write(fake_signature)
        
        # Tenter la vérification
        is_valid, message = self.verifier.verify_file(file_path, target_signature_path)
        
        # Restaurer la signature originale
        with open(target_signature_path, 'w') as f:
            f.write(original_signature)
        
        result = {
            "attack_type": "signature_replacement",
            "file": str(file_path),
            "signature": str(target_signature_path),
            "detected": not is_valid,
            "message": message,
            "success": True
        }
        
        self.attack_results.append(result)
        return result
    
    def simulate_man_in_the_middle(self, update_file: Union[str, Path],signature_path: Union[str, Path]) -> Dict:
    
        # Simule une attaque Man-in-the-Middle sur le canal de mise à jour
        update_file = Path(update_file)
        signature_path = Path(signature_path)
        
        # Sauvegarder les originaux
        with open(update_file, 'rb') as f:
            original_update = f.read()
        
        with open(signature_path, 'r') as f:
            original_signature = f.read()
        
        # Attaque: remplacer le fichier ET la signature
        # Créer un fichier malveillant
        malicious_content = b"#!/bin/bash\necho 'MALICIOUS CODE EXECUTED'\n"
        with open(update_file, 'wb') as f:
            f.write(malicious_content)
        
        # Créer une fausse signature
        fake_signature = self._create_fake_signature(update_file)
        with open(signature_path, 'w') as f:
            f.write(fake_signature)
        
        # Vérification
        is_valid, message = self.verifier.verify_file(update_file, signature_path)
        
        # Restaurer
        with open(update_file, 'wb') as f:
            f.write(original_update)
        with open(signature_path, 'w') as f:
            f.write(original_signature)
        
        result = {
            "attack_type": "man_in_the_middle",
            "file": str(update_file),
            "detected": not is_valid,
            "message": message,
            "success": True
        }
        
        self.attack_results.append(result)
        return result
    
    def _create_fake_signature(self, file_path: Path) -> str:
        
        # Crée une fausse signature (format valide mais signature invalide)
        
        import json
        from datetime import datetime
        
        fake_manifest = {
            "file": str(file_path),
            "filename": file_path.name,
            "signature": "ZmFrZV9zaWduYXR1cmVfdGhhdF9pc19pbnZhbGlk" * 10,  # Fausse signature
            "algorithm": "Ed25519",
            "hash_algorithm": "SHA256",
            "timestamp": datetime.now().isoformat(),
            "file_size": file_path.stat().st_size if file_path.exists() else 0,
            "note": "FAKE SIGNATURE - ATTACK SIMULATION"
        }
        
        return json.dumps(fake_manifest, indent=2)
    
    def run_all_attacks(self, test_file: Union[str, Path]) -> Dict:
        """
        Exécute toutes les simulations d'attaques
        
        Args:
            test_file: Fichier de test à utiliser
            
        Returns:
            Dict: Résumé des résultats
        """
        print("\n" + "="*60)
        print(" SIMULATION D'ATTAQUES SUR LA SIGNATURE DE CODE")
        print("="*60)
        
        test_file = Path(test_file)
        signature_file = test_file.with_suffix(test_file.suffix + '.sig')
        
        attacks = [
            ("Modification du fichier", lambda: self.simulate_file_modification(test_file)),
            ("Remplacement de signature", lambda: self.simulate_signature_replacement(test_file, signature_file)),
            ("Man-in-the-Middle", lambda: self.simulate_man_in_the_middle(test_file, signature_file))
        ]
        
        for attack_name, attack_func in attacks:
            print(f"\n Simulation: {attack_name}")
            print("-" * 40)
            result = attack_func()
            
            if result.get('detected', False):
                print(f" Attaque DÉTECTÉE: {result['message']}")
            else:
                print(f" Attaque NON DÉTECTÉE - Faille potentielle!")
        
        # Résumé
        print("\n" + "="*60)
        print("RÉSUMÉ DES ATTAQUES")
        print("="*60)
        
        detected = sum(1 for r in self.attack_results if r.get('detected', False))
        total = len(self.attack_results)
        
        print(f"Attaques détectées: {detected}/{total}")
        print(f"Taux de détection: {(detected/total)*100:.1f}%")
        
        return {
            "total_attacks": total,
            "detected": detected,
            "results": self.attack_results
        }