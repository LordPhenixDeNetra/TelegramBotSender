import sqlite3
import json
import os
from datetime import datetime

class Database:
    def __init__(self, db_file='bootsender.db'):
        self.db_file = db_file
        self.init_db()

    def init_db(self):
        """Initialise la base de données avec les tables nécessaires"""
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            
            # Table des destinataires
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS recipients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    chat_id INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Table des envois de fichiers
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS file_sends (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    recipient_id INTEGER,
                    file_name TEXT NOT NULL,
                    file_path TEXT NOT NULL,
                    status TEXT NOT NULL,
                    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (recipient_id) REFERENCES recipients (id)
                )
            ''')
            
            conn.commit()

    def add_recipient(self, name, chat_id):
        """Ajoute un nouveau destinataire"""
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'INSERT INTO recipients (name, chat_id) VALUES (?, ?)',
                    (name, chat_id)
                )
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            return False

    def get_all_recipients(self):
        """Récupère tous les destinataires"""
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT name, chat_id FROM recipients')
            return {row[0]: row[1] for row in cursor.fetchall()}

    def delete_recipient(self, name):
        """Supprime un destinataire"""
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM recipients WHERE name = ?', (name,))
            conn.commit()
            return cursor.rowcount > 0

    def log_file_send(self, recipient_name, file_path, status):
        """Enregistre un envoi de fichier"""
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            # Récupérer l'ID du destinataire
            cursor.execute('SELECT id FROM recipients WHERE name = ?', (recipient_name,))
            recipient_id = cursor.fetchone()[0]
            
            cursor.execute('''
                INSERT INTO file_sends (recipient_id, file_name, file_path, status)
                VALUES (?, ?, ?, ?)
            ''', (recipient_id, os.path.basename(file_path), file_path, status))
            conn.commit()

    def get_send_history(self, limit=50):
        """Récupère l'historique des envois"""
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT r.name, f.file_name, f.status, f.sent_at
                FROM file_sends f
                JOIN recipients r ON f.recipient_id = r.id
                ORDER BY f.sent_at DESC
                LIMIT ?
            ''', (limit,))
            return cursor.fetchall()

    def import_users_from_json(self, users_dict):
        """Importe les utilisateurs depuis un dictionnaire"""
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            for name, chat_id in users_dict.items():
                try:
                    cursor.execute(
                        'INSERT INTO recipients (name, chat_id) VALUES (?, ?)',
                        (name, chat_id)
                    )
                except sqlite3.IntegrityError:
                    # Mettre à jour si le nom existe déjà
                    cursor.execute(
                        'UPDATE recipients SET chat_id = ? WHERE name = ?',
                        (chat_id, name)
                    )
            conn.commit()