#!/usr/bin/env python3
"""
Script de build pour créer un exécutable de BootSender
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def clean_build_dirs():
    """Nettoie les répertoires de build précédents"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"🧹 Nettoyage du répertoire {dir_name}...")
            shutil.rmtree(dir_name)

def build_executable():
    """Construit l'exécutable avec PyInstaller"""
    print("🔨 Construction de l'exécutable BootSender...")
    
    # Options PyInstaller
    cmd = [
        'pyinstaller',
        '--onefile',                    # Un seul fichier exécutable
        '--windowed',                   # Pas de console (pour GUI)
        '--name=BootSender',            # Nom de l'exécutable
        '--icon=icon.ico',              # Icône (si disponible)
        '--add-data=bootsender.db;.',   # Inclure la base de données
        '--hidden-import=tkinter',      # Import caché pour tkinter
        '--hidden-import=sqlite3',      # Import caché pour sqlite3
        '--hidden-import=asyncio',      # Import caché pour asyncio
        'main.py'                       # Fichier principal
    ]
    
    # Retirer l'icône si elle n'existe pas
    if not os.path.exists('icon.ico'):
        cmd.remove('--icon=icon.ico')
        print("⚠️  Aucune icône trouvée, construction sans icône")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Exécutable créé avec succès!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de la construction: {e}")
        print(f"Sortie d'erreur: {e.stderr}")
        return False

def copy_dependencies():
    """Copie les fichiers nécessaires dans le répertoire dist"""
    print("📁 Copie des dépendances...")
    
    files_to_copy = [
        'config.py',
        'database.py',
        'bootsender.db'
    ]
    
    dist_dir = Path('dist')
    if not dist_dir.exists():
        print("❌ Répertoire dist non trouvé!")
        return False
    
    for file_name in files_to_copy:
        if os.path.exists(file_name):
            shutil.copy2(file_name, dist_dir)
            print(f"✅ {file_name} copié")
        else:
            print(f"⚠️  {file_name} non trouvé")
    
    return True

def create_installer_info():
    """Crée un fichier d'information pour l'installation"""
    info_content = """
# BootSender - Exécutable

## Installation
1. Copiez le fichier BootSender.exe où vous voulez
2. Assurez-vous que les fichiers suivants sont dans le même répertoire :
   - config.py (avec votre token Telegram)
   - database.py
   - bootsender.db

## Utilisation
Double-cliquez sur BootSender.exe pour lancer l'application.

## Configuration
Modifiez le fichier config.py avec votre token de bot Telegram avant la première utilisation.
"""
    
    with open('dist/INSTALLATION.txt', 'w', encoding='utf-8') as f:
        f.write(info_content)
    
    print("✅ Fichier d'installation créé")

def main():
    """Fonction principale du script de build"""
    print("🚀 Début de la construction de l'exécutable BootSender")
    print("=" * 50)
    
    # Vérifier que nous sommes dans le bon répertoire
    if not os.path.exists('main.py'):
        print("❌ Fichier main.py non trouvé! Assurez-vous d'être dans le bon répertoire.")
        sys.exit(1)
    
    # Nettoyer les anciens builds
    clean_build_dirs()
    
    # Construire l'exécutable
    if not build_executable():
        print("❌ Échec de la construction de l'exécutable")
        sys.exit(1)
    
    # Copier les dépendances
    if not copy_dependencies():
        print("❌ Échec de la copie des dépendances")
        sys.exit(1)
    
    # Créer les informations d'installation
    create_installer_info()
    
    print("=" * 50)
    print("🎉 Construction terminée avec succès!")
    print("📁 L'exécutable se trouve dans le répertoire 'dist/'")
    print("📋 Lisez le fichier INSTALLATION.txt pour les instructions")

if __name__ == "__main__":
    main()