#!/usr/bin/env python3

import sys
# Script exemple simple pour tester la signature
def main():
    print("=" * 50)
    print("Hello World from Signed Application!")
    print("=" * 50)
    print("Cette application a été signée avec Ed25519")
    print("La signature a été vérifiée avec succès")
    
    if len(sys.argv) > 1:
        print(f"\nArguments reçus: {sys.argv[1:]}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())