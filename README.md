# BootSender - Envoi de fichiers vers Telegram

## Description

BootSender est une application de bureau développée en Python qui permet d'envoyer facilement des fichiers vers Telegram. L'application offre une interface graphique intuitive construite avec Tkinter pour gérer l'envoi de fichiers vers des utilisateurs ou groupes Telegram.

## Fonctionnalités

- 📤 Envoi de fichiers vers Telegram
- 👥 Gestion des destinataires (utilisateurs et groupes)
- 📊 Historique des envois
- 🎨 Interface graphique moderne avec Tkinter
- 💾 Base de données SQLite pour la persistance des données
- 🔧 Configuration simple du bot Telegram

## Prérequis

- Python 3.8 ou supérieur
- Un bot Telegram (token requis)
- Les dépendances listées dans `requirements.txt`

## Installation

1. Clonez ou téléchargez le projet :
```bash
git clone <url-du-repo>
cd BootSender
```

2. Créez un environnement virtuel (recommandé) :
```bash
python -m venv venv
```

3. Activez l'environnement virtuel :
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. Installez les dépendances :
```bash
pip install -r requirements.txt
```

## Configuration

1. Créez un bot Telegram via [@BotFather](https://t.me/botfather)
2. Récupérez le token de votre bot
3. Modifiez le fichier `config.py` avec votre token :
```python
BOT_TOKEN = "VOTRE_TOKEN_ICI"
```

## Utilisation

### Option 1 : Exécutable (Recommandé)
1. Téléchargez l'exécutable depuis le répertoire `dist/`
2. Double-cliquez sur `BootSender.exe`
3. L'application se lance directement sans installation Python

### Option 2 : Code source Python
1. Lancez l'application :
```bash
python main.py
```

2. L'interface graphique s'ouvrira avec les options suivantes :
   - **Sélection de fichier** : Choisissez le fichier à envoyer
   - **Destinataires** : Sélectionnez les utilisateurs/groupes destinataires
   - **Envoi** : Lancez l'envoi du fichier
   - **Historique** : Consultez l'historique des envois

## Création de l'exécutable

Pour créer votre propre exécutable :

1. Installez PyInstaller :
```bash
pip install pyinstaller
```

2. Utilisez le script de build automatisé :
```bash
python build_exe.py
```

3. L'exécutable sera créé dans le répertoire `dist/`

## Structure du projet

```
BootSender/
├── main.py           # Point d'entrée de l'application
├── config.py         # Configuration (token bot, etc.)
├── database.py       # Gestion de la base de données SQLite
├── bootsender.db     # Base de données SQLite
├── build_exe.py      # Script de build pour l'exécutable
├── requirements.txt  # Dépendances Python
├── .gitignore       # Fichiers à ignorer par Git
├── README.md        # Documentation
└── dist/            # Répertoire contenant l'exécutable
    ├── BootSender.exe      # Exécutable principal
    ├── INSTALLATION.txt    # Instructions d'installation
    ├── config.py          # Configuration
    ├── database.py        # Module base de données
    └── bootsender.db      # Base de données
```

## Base de données

L'application utilise SQLite pour stocker :
- Les informations des destinataires
- L'historique des envois
- Les configurations utilisateur

## Dépannage

### L'application se ferme immédiatement
- Vérifiez que toutes les dépendances sont installées
- Assurez-vous que le token du bot est correct dans `config.py`
- Consultez les messages d'erreur dans la console

### Erreur de connexion Telegram
- Vérifiez votre connexion internet
- Assurez-vous que le token du bot est valide
- Vérifiez que le bot n'est pas bloqué

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer de nouvelles fonctionnalités
- Améliorer la documentation

## Licence

Ce projet est sous licence libre. Vous pouvez l'utiliser, le modifier et le distribuer selon vos besoins.

## Support

Pour toute question ou problème, n'hésitez pas à ouvrir une issue ou à contacter les développeurs.