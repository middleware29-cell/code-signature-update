
# Politique de mise à jour sécurisée avec vérification de signature


import os
import shutil
from pathlib import Path
from typing import Union, Optional, Callable
from dataclasses import dataclass
from datetime import datetime
import json

@dataclass
class UpdateResult:
    # Résultat d'une tentative de mise à jour
    success: bool
    message: str
    timestamp: datetime
    backup_path: Optional[Path] = None

class UpdatePolicy:
    
    # Implémente la politique de mise à jour : refuser l'exécution/mise à jour si signature invalide
    
    def __init__(self, verifier, backup_enabled: bool = True):
        
        # Initialise la politique de mise à jour
        
        self.verifier = verifier
        self.backup_enabled = backup_enabled
        self.update_log = []
        
    def apply_update(self, update_file: Union[str, Path],target_location: Union[str, Path],signature_path: Optional[Union[str, Path]] = None) -> UpdateResult:
        
        # Applique une mise à jour après vérification de signature
        update_file = Path(update_file)
        target_location = Path(target_location)
        
        # Étape 1: Vérifier la signature
        print(f"\nVérification de la signature de {update_file.name}...")
        is_valid, message = self.verifier.verify_file(update_file, signature_path)
        
        if not is_valid:
            print(f" Mise à jour REFUSÉE: {message}")
            return UpdateResult(
                success=False,
                message=f"Signature invalide: {message}",
                timestamp=datetime.now()
            )
        
        print(f" Signature vérifiée avec succès")
        
        # Étape 2: Créer une sauvegarde si demandé
        backup_path = None
        if self.backup_enabled and target_location.exists():
            backup_path = target_location.with_suffix(target_location.suffix + '.backup')
            shutil.copy2(target_location, backup_path)
            print(f" Sauvegarde créée: {backup_path}")
        
        # Étape 3: Appliquer la mise à jour
        try:
            shutil.copy2(update_file, target_location)
            print(f" Mise à jour appliquée: {target_location}")
            
            result = UpdateResult(
                success=True,
                message="Mise à jour appliquée avec succès",
                timestamp=datetime.now(),
                backup_path=backup_path
            )
        except Exception as e:
            result = UpdateResult(
                success=False,
                message=f"Erreur lors de l'application: {str(e)}",
                timestamp=datetime.now(),
                backup_path=backup_path
            )
        
        # Journaliser
        self._log_update(result, update_file, target_location)
        
        return result
    
    def verify_and_execute(self, executable_file: Union[str, Path],signature_path: Optional[Union[str, Path]] = None) -> bool:
    
         # Vérifie la signature avant exécution
        executable_file = Path(executable_file)
        
        print(f"\nVérification pré-exécution de {executable_file.name}...")
        is_valid, message = self.verifier.verify_file(executable_file, signature_path)
        
        if is_valid:
            print(f"{message}")
            print(f"Exécution autorisée")
            return True
        else:
            print(f" {message}")
            print(f" Exécution REFUSÉE - Signature invalide")
            return False
    
    def _log_update(self, result: UpdateResult, update_file: Path, target: Path):

        #Journalise les tentatives de mise à jour
        log_entry = {
            "timestamp": result.timestamp.isoformat(),
            "success": result.success,
            "message": result.message,
            "update_file": str(update_file),
            "target": str(target),
            "backup": str(result.backup_path) if result.backup_path else None
        }
        
        self.update_log.append(log_entry)
        
        # Sauvegarder le log
        log_file = Path("update_log.json")
        existing_logs = []
        if log_file.exists():
            with open(log_file, 'r') as f:
                existing_logs = json.load(f)
        
        existing_logs.append(log_entry)
        with open(log_file, 'w') as f:
            json.dump(existing_logs, f, indent=2)
    
    def rollback(self, target_location: Union[str, Path]) -> bool:
    
         # Restaure la dernière sauvegarde
        target_location = Path(target_location)
        backup_path = target_location.with_suffix(target_location.suffix + '.backup')
        
        if not backup_path.exists():
            print(f" Aucune sauvegarde trouvée pour {target_location}")
            return False
        
        try:
            shutil.copy2(backup_path, target_location)
            print(f"Restauration effectuée depuis {backup_path}")
            return True
        except Exception as e:
            print(f"Erreur lors de la restauration: {str(e)}")
            return False