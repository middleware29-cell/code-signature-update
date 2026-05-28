#!/usr/bin/env python3
"""
================================================================================
MON APPLICATION - TEST DE SIGNATURE ED25519
================================================================================
Ce fichier sert à tester le système de signature cryptographique.
Auteur: Master 1 Cybersécurité
Version: 1.0.0
================================================================================
"""

import sys
import os
from datetime import datetime

def afficher_entete():
    """Affiche l'en-tête de l'application"""
    print("=" * 60)
    print("   APPLICATION DE TEST - SIGNATURE ED25519")
    print("=" * 60)
    print(f"   Date : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"   Utilisateur : {os.getlogin() if hasattr(os, 'getlogin') else 'Inconnu'}")
    print("=" * 60)
    print()

def afficher_menu():
    """Affiche le menu principal"""
    print("Menu principal :")
    print("1. Afficher un message de bienvenue")
    print("2. Calculer une somme")
    print("3. Afficher la date et l'heure")
    print("4. Quitter")
    print()

def message_bienvenue():
    """Affiche un message de bienvenue"""
    print("\n" + "=" * 40)
    print("   BIENVENUE DANS MON APPLICATION !")
    print("=" * 40)
    print("   Cette application a été signée avec Ed25519.")
    print("   La signature a été vérifiée avec succès.")
    print("   Aucune modification malveillante n'a été détectée.")
    print("=" * 40 + "\n")

def calculer_somme():
    """Demande deux nombres et affiche leur somme"""
    try:
        a = float(input("Entrez le premier nombre : "))
        b = float(input("Entrez le deuxième nombre : "))
        print(f"\nRésultat : {a} + {b} = {a + b}\n")
    except ValueError:
        print("\nErreur : Veuillez entrer des nombres valides !\n")

def afficher_date_heure():
    """Affiche la date et l'heure actuelles"""
    maintenant = datetime.now()
    print("\n" + "=" * 40)
    print(f"   Date : {maintenant.strftime('%d/%m/%Y')}")
    print(f"   Heure : {maintenant.strftime('%H:%M:%S')}")
    print("=" * 40 + "\n")

def main():
    """Fonction principale de l'application"""
    afficher_entete()
    
    while True:
        afficher_menu()
        choix = input("Votre choix : ")
        
        if choix == "1":
            message_bienvenue()
        elif choix == "2":
            calculer_somme()
        elif choix == "3":
            afficher_date_heure()
        elif choix == "4":
            print("\nAu revoir !\n")
            break
        else:
            print("\nChoix invalide. Veuillez réessayer.\n")
    

if __name__ == "__main__":
    main()