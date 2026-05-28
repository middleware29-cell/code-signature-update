#!/usr/bin/env python3
"""
Système de signature de code pour mises à jour applicatives
Utilisation des clés Ed25519 via PyNaCl.


Auteur:     TADJUIDJE KAMDEM ANDRE JORDAN     21T2472

            ONGONO MVEME BERTRAND             09U0529

            
Date: 2025-2026
"""

import sys
import os
import argparse
from pathlib import Path

# Ajouter src au path
sys.path.insert(0, str(Path(__file__).parent))

from src.key_manager import KeyManager
from src.signer import FileSigner
from src.verifier import SignatureVerifier
from src.update_policy import UpdatePolicy
from src.attack_simulator import AttackSimulator

def setup_keys(key_manager, key_name="update_key"):
    """Génère ou charge les clés"""
    print("\nGESTION DES CLÉS")
    print("="*40)
    
    key_path = Path("keys") / f"{key_name}_private.key"
    
    if key_path.exists():
        print(f"✓ Clés existantes trouvées pour '{key_name}'")
        private_key = key_manager.load_private_key(key_name)
        public_key = key_manager.load_public_key(key_name)
    else:
        print(f"Génération d'une nouvelle paire de clés '{key_name}'...")
        private_key, public_key = key_manager.generate_keypair(key_name)
        print(f"Clés générées avec succès")
    
    # Afficher la clé publique
    public_key_b64 = key_manager.export_public_key(key_name)
    print(f"\nClé publique (à distribuer):")
    print(f"{public_key_b64[:64]}...")
    
    return private_key, public_key

def sign_file_example(signer, file_path):
    """Exemple de signature de fichier"""
    print(f"\nSIGNATURE DU FICHIER")
    print("="*40)
    
    if not Path(file_path).exists():
        print(f"Fichier non trouvé: {file_path}")
        return False
    
    try:
        signature = signer.sign_file(file_path)
        print(f"\n Signature réussie!")
        return True
    except Exception as e:
        print(f"Erreur: {str(e)}")
        return False

def verify_file_example(verifier, file_path):
    """Exemple de vérification de fichier"""
    print(f"\nVÉRIFICATION DU FICHIER")
    print("="*40)
    
    if not Path(file_path).exists():
        print(f"Fichier non trouvé: {file_path}")
        return False
    
    is_valid, message = verifier.verify_file(file_path)
    print(f"\n{message}")
    return is_valid

def update_example(update_policy, update_file, target_file):
    """Exemple de mise à jour sécurisée"""
    print(f"\nMISE À JOUR SÉCURISÉE")
    print("="*40)
    
    result = update_policy.apply_update(update_file, target_file)
    
    if result.success:
        print(f"\n{result.message}")
    else:
        print(f"\n{result.message}")
    
    return result.success

def attack_simulation_example(attack_simulator, test_file):
    """Exemple de simulation d'attaque"""
    print(f"\n  SIMULATION D'ATTAQUES")
    print("="*40)
    
    results = attack_simulator.run_all_attacks(test_file)
    return results

def create_test_file():
    """Crée un fichier de test"""
    test_file = Path("test_update.py")
    test_content = '''#!/usr/bin/env python3
"""
Script de test pour mise à jour applicative
"""

def main():
    print("Application de test - Version sécurisée")
    print("Cette application a été vérifiée par signature cryptographique")
    
if __name__ == "__main__":
    main()
'''
    
    with open(test_file, 'w') as f:
        f.write(test_content)
    
    # Rendre exécutable sur Linux/Mac
    if sys.platform != 'win32':
        os.chmod(test_file, 0o755)
    
    print(f"✓ Fichier de test créé: {test_file}")
    return test_file

def main():
    parser = argparse.ArgumentParser(description="Système de signature de code avec Ed25519",formatter_class=argparse.RawDescriptionHelpFormatter,epilog="""
Exemples d'utilisation:
  python main.py setup          # Génère les clés
  python main.py sign test.py   # Signe un fichier
  python main.py verify test.py # Vérifie un fichier
  python main.py update test.py target.py # Mise à jour sécurisée
  python main.py attack test.py # Simule des attaques
  python main.py demo           # Démonstration complète
        """
    )
    
    parser.add_argument("command", choices=["setup", "sign", "verify", "update", "attack", "demo"],help="Commande à exécuter")
    parser.add_argument("file", nargs="?", help="Fichier cible")
    parser.add_argument("target", nargs="?", help="Destination (pour update)")
    
    args = parser.parse_args()
    
    # Initialisation des composants
    key_manager = KeyManager()
    
    if args.command == "setup":
        private_key, public_key = setup_keys(key_manager)
        print("\nConfiguration terminée")
        
    elif args.command == "sign":
        if not args.file:
            print("Spécifiez un fichier à signer")
            return
        
        private_key, public_key = setup_keys(key_manager)
        signer = FileSigner(private_key)
        sign_file_example(signer, args.file)
        
    elif args.command == "verify":
        if not args.file:
            print("Spécifiez un fichier à vérifier")
            return
        
        private_key, public_key = setup_keys(key_manager)
        verifier = SignatureVerifier(public_key)
        verify_file_example(verifier, args.file)
        
    elif args.command == "update":
        if not args.file or not args.target:
            print("Usage: python main.py update <fichier_update> <cible>")
            return
        
        private_key, public_key = setup_keys(key_manager)
        verifier = SignatureVerifier(public_key)
        update_policy = UpdatePolicy(verifier)
        update_example(update_policy, args.file, args.target)
        
    elif args.command == "attack":
        if not args.file:
            print("Spécifiez un fichier de test")
            return
        
        private_key, public_key = setup_keys(key_manager)
        verifier = SignatureVerifier(public_key)
        
        # S'assurer que le fichier est signé
        signer = FileSigner(private_key)
        sign_file_example(signer, args.file)
        
        attack_sim = AttackSimulator(verifier)
        attack_simulation_example(attack_sim, args.file)
        
    elif args.command == "demo":
        print("\n" + "="*60)
        print("DÉMONSTRATION COMPLÈTE - SIGNATURE DE CODE")
        print("="*60)
        
        # 1. Configuration
        private_key, public_key = setup_keys(key_manager)
        
        # 2. Créer un fichier de test
        test_file = create_test_file()
        
        # 3. Signer le fichier
        signer = FileSigner(private_key)
        sign_file_example(signer, test_file)
        
        # 4. Vérifier le fichier (devrait réussir)
        verifier = SignatureVerifier(public_key)
        print("\n--- Test 1: Vérification normale ---")
        verify_file_example(verifier, test_file)
        
        # 5. Simuler une attaque
        attack_sim = AttackSimulator(verifier)
        attack_simulation_example(attack_sim, test_file)
        
        # 6. Politique de mise à jour
        update_policy = UpdatePolicy(verifier)
        target_file = Path("installed_app.py")
        
        print("\n--- Test 2: Mise à jour sécurisée ---")
        update_example(update_policy, test_file, target_file)
        
        print("\n" + "="*60)
        print("DÉMONSTRATION TERMINÉE")
        print("="*60)

if __name__ == "__main__":
    main()