#!/usr/bin/env python3
"""
Fichier malveillant pour simuler une attaque
Ce fichier ne devrait PAS être signé par la clé officielle
"""
import os
import subprocess

def malicious_action():
    """Simule une action malveillante"""
    print(" ATTENTION: Ceci est un fichier NON AUTORISÉ!")
    print("Tentative d'exécution de code malveillant...")
    
    # Simulation d'action malveillante (sans réelle action dangereuse)
    print("-> Modification de configuration détectée")
    print("-> Injection de code tentée")
    
    return False

if __name__ == "__main__":
    malicious_action()