# Code Signature System with Ed25519


Système de signature cryptographique pour mises à jour applicatives utilisant Ed25519 via PyNaCl.

## Table des matières

1. Structure du projet
2. Installation
3. Utilisation via Interface Web Streamlit ou via Terminal
4. Commandes
5. Tests
---

##    1.   Structure du projet

code-signature-update/
│
├── src/                           # Code source
│   ├── __init__.py
│   ├── key_manager.py             # Génération et gestion des clés
│   ├── signer.py                  # Signature des fichiers
│   ├── verifier.py                # Vérification des signatures
│   ├── update_policy.py           # Politique de mise à jour sécurisée
│   └── attack_simulator.py        # Simulation d'attaques
│
├── tests/                         # Tests unitaires
│   ├── test_attack.py
│   ├── test_signer.py
│   └── test_verifier.py
│
├── examples/                      # Fichiers d'exemple
│   ├── hello_world.py
│   ├── update_script.py
│   ├── malicious_file.py
│   ├── unsigned_script.py
│   └── config.json
│
├── keys/                          # Clés cryptographiques (générées)
│   ├── update_key_private.key     #  À garder SECRET
│   ├── update_key_public.key      #  À distribuer
│   └── update_key_metadata.json
│
├── uploads/                       # Fichiers uploadés (Streamlit)
│
├── app.py                         # Interface web Streamlit
├── main.py                        # Interface ligne de commande
├── requirements.txt               # Dépendances Python
├── LICENSE                        # Licence MIT
└── README.md                      # Documentation
---


##   2. Installation


### Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Étapes d'installation


# 1. Cloner le dépôt
git clone https://github.com/votre-username/code-signature-update.git
cd code-signature-update

# 2. Créer l'environnement virtuel
python3 -m venv venv

# 3. Activer l'environnement virtuel
source venv/bin/activate

# 4. Installer les dépendances
pip install -r requirements.txt

---



### 3.  Utilisation via Interface Web Streamlit  ou via terminal
         


  ###  A.  Utilisation via Interface Web Streamlit

 streamlit run app.py













   ### B. utilisation via terminal


### Commande	Description

setup	Génère une paire de clés Ed25519
sign <fichier>	Signe un fichier
verify <fichier>	Vérifie la signature
update <src> <dst>	Mise à jour sécurisée
attack <fichier>	Simule des attaques
demo	Démonstration complète






# Générer les clés
python main.py setup

# Signer un fichier
python main.py sign examples/hello_world.py

# Vérifier une signature
python main.py verify examples/hello_world.py

# Simuler des attaques
python main.py attack examples/hello_world.py

# Démonstration complète
python main.py demo

# Mise à jour sécurisée
python3 main.py update test_update.py installed_app.py






 ###  Tests



   # Exécuter les tests unitaires
        python -m pytest tests/ -v

   # Avec couverture
        python -m pytest tests/ --cov=src


   # Exécuter tous les tests
         python3 -m pytest tests/ -v


