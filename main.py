import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from telegram import Bot
import asyncio
from config import BOT_TOKEN, INITIAL_USERS, DB_FILE
from database import Database
import os
import sys

class FileSenderApp:
    def __init__(self, root):
        print("Initialisation de l'application...")  # Debug
        self.root = root
        self.root.title("BootSender - Envoi de fichiers vers Telegram")
        self.root.geometry("800x800")
        
        # Configuration du style
        print("Configuration du style...")  # Debug
        style = ttk.Style()
        style.configure('Accent.TButton', background='#2196F3')
        print("Style configuré avec succès")  # Debug
        
        # Initialisation du bot et de la base de données
        print("Initialisation du bot et de la base de données...")  # Debug
        try:
            self.bot = Bot(token=BOT_TOKEN)
            print("Bot initialisé avec succès")  # Debug
            self.db = Database(DB_FILE)
            print("Base de données initialisée avec succès")  # Debug
        except Exception as e:
            print(f"Erreur lors de l'initialisation : {str(e)}", file=sys.stderr)  # Debug
            raise
        
        # Importer les utilisateurs initiaux
        print("Import des utilisateurs initiaux...")  # Debug
        try:
            self.db.import_users_from_json(INITIAL_USERS)
            print("Utilisateurs importés avec succès")  # Debug
        except Exception as e:
            print(f"Erreur lors de l'import des utilisateurs : {str(e)}", file=sys.stderr)  # Debug
            raise
        
        # Liste pour stocker les fichiers sélectionnés
        self.selected_files = []
        
        # Création des widgets
        print("Création des widgets...")  # Debug
        try:
            self.create_widgets()
            print("Widgets créés avec succès")  # Debug
        except Exception as e:
            print(f"Erreur lors de la création des widgets : {str(e)}", file=sys.stderr)  # Debug
            raise

        print("Initialisation de l'application terminée avec succès")  # Debug

    def create_widgets(self):
        print("Création de la frame principale...")  # Debug
        # Frame principale
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        print("Création du titre...")  # Debug
        # Titre
        title_label = ttk.Label(
            main_frame,
            text="Sélectionnez les fichiers à envoyer",
            font=('Helvetica', 14, 'bold')
        )
        title_label.pack(pady=10)

        print("Création de la frame des destinataires...")  # Debug
        # Frame pour la sélection des destinataires
        recipient_frame = ttk.LabelFrame(
            main_frame,
            text="Destinataires"
        )
        recipient_frame.pack(fill=tk.X, pady=10)

        # Frame pour les boutons de sélection des destinataires
        recipient_buttons_frame = ttk.Frame(recipient_frame)
        recipient_buttons_frame.pack(fill=tk.X, padx=5, pady=5)

        # Boutons pour sélectionner/désélectionner tous les destinataires
        select_all_button = ttk.Button(
            recipient_buttons_frame,
            text="Tout sélectionner",
            command=self.select_all_recipients,
            style='Accent.TButton'
        )
        select_all_button.pack(side=tk.LEFT, padx=2)

        deselect_all_button = ttk.Button(
            recipient_buttons_frame,
            text="Tout désélectionner",
            command=self.deselect_all_recipients,
            style='Accent.TButton'
        )
        deselect_all_button.pack(side=tk.LEFT, padx=2)

        print("Création de la liste des destinataires...")  # Debug
        # Frame pour la liste des destinataires
        self.recipients_list_frame = ttk.Frame(recipient_frame)
        self.recipients_list_frame.pack(fill=tk.X, padx=5)

        # Liste des destinataires avec cases à cocher
        self.recipient_vars = {}
        self.update_recipients_list()

        print("Création du formulaire d'ajout de destinataire...")  # Debug
        # Frame pour ajouter un nouveau destinataire
        add_recipient_frame = ttk.Frame(recipient_frame)
        add_recipient_frame.pack(fill=tk.X, padx=5, pady=5)

        # Champs pour ajouter un nouveau destinataire
        ttk.Label(add_recipient_frame, text="Nom:").pack(side=tk.LEFT, padx=2)
        self.new_recipient_name = ttk.Entry(add_recipient_frame, width=20)
        self.new_recipient_name.pack(side=tk.LEFT, padx=2)

        ttk.Label(add_recipient_frame, text="Chat ID:").pack(side=tk.LEFT, padx=2)
        self.new_recipient_id = ttk.Entry(add_recipient_frame, width=15)
        self.new_recipient_id.pack(side=tk.LEFT, padx=2)

        add_button = ttk.Button(
            add_recipient_frame,
            text="Ajouter",
            command=self.add_recipient,
            style='Accent.TButton'
        )
        add_button.pack(side=tk.LEFT, padx=2)

        print("Création des boutons de sélection de fichiers...")  # Debug
        # Frame pour les boutons de sélection et de nettoyage
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=5)

        # Bouton pour sélectionner les fichiers
        select_button = ttk.Button(
            button_frame,
            text="Sélectionner des fichiers",
            command=self.select_files,
            style='Accent.TButton'
        )
        select_button.pack(side=tk.LEFT, padx=5)

        # Bouton pour effacer la liste
        clear_button = ttk.Button(
            button_frame,
            text="Effacer la liste",
            command=self.clear_files,
            style='Accent.TButton'
        )
        clear_button.pack(side=tk.RIGHT, padx=5)

        print("Création de la liste des fichiers...")  # Debug
        # Liste des fichiers avec label
        files_label = ttk.Label(
            main_frame,
            text="Fichiers sélectionnés :",
            font=('Helvetica', 10, 'bold')
        )
        files_label.pack(fill=tk.X, padx=5, pady=(10, 0))

        # Frame pour la liste des fichiers
        files_frame = ttk.Frame(main_frame)
        files_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        # Scrollbar pour la liste des fichiers
        files_scrollbar = ttk.Scrollbar(files_frame)
        files_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.files_listbox = tk.Listbox(
            files_frame,
            width=50,
            height=10,
            selectmode=tk.MULTIPLE,
            bg='white',
            font=('Helvetica', 10),
            yscrollcommand=files_scrollbar.set
        )
        self.files_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        files_scrollbar.config(command=self.files_listbox.yview)

        print("Création de la barre de progression...")  # Debug
        # Barre de progression
        self.progress_frame = ttk.Frame(main_frame)
        self.progress_frame.pack(fill=tk.X, pady=5)

        self.progress_label = ttk.Label(
            self.progress_frame,
            text="Progression : 0%"
        )
        self.progress_label.pack()

        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            orient='horizontal',
            length=300,
            mode='determinate'
        )
        self.progress_bar.pack(pady=5)

        print("Création de l'historique des envois...")  # Debug
        # Historique des envois
        history_frame = ttk.LabelFrame(
            main_frame,
            text="Historique des envois"
        )
        history_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Frame pour le tableau d'historique
        history_tree_frame = ttk.Frame(history_frame)
        history_tree_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        # Scrollbar pour le tableau d'historique
        history_scrollbar = ttk.Scrollbar(history_tree_frame)
        history_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Tableau d'historique
        self.history_tree = ttk.Treeview(
            history_tree_frame,
            columns=('date', 'destinataire', 'fichier', 'statut'),
            show='headings',
            height=5,
            yscrollcommand=history_scrollbar.set
        )

        # Configuration des colonnes
        self.history_tree.heading('date', text='Date')
        self.history_tree.heading('destinataire', text='Destinataire')
        self.history_tree.heading('fichier', text='Fichier')
        self.history_tree.heading('statut', text='Statut')

        self.history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        history_scrollbar.config(command=self.history_tree.yview)

        # Bouton pour actualiser l'historique
        refresh_button = ttk.Button(
            history_frame,
            text="Actualiser l'historique",
            command=self.update_history,
            style='Accent.TButton'
        )
        refresh_button.pack(pady=5)

        print("Création du bouton d'envoi...")  # Debug
        # Bouton pour envoyer les fichiers
        send_button = ttk.Button(
            main_frame,
            text="Envoyer les fichiers",
            command=self.send_files,
            style='Accent.TButton'
        )
        send_button.pack(pady=10)

        print("Chargement de l'historique initial...")  # Debug
        # Charger l'historique initial
        self.update_history()
        print("Création des widgets terminée avec succès")  # Debug

    def update_recipients_list(self):
        print("Mise à jour de la liste des destinataires...")  # Debug
        # Nettoyer la frame existante
        for widget in self.recipients_list_frame.winfo_children():
            widget.destroy()

        # Récupérer les destinataires depuis la base de données
        recipients = self.db.get_all_recipients()
        print(f"Destinataires récupérés : {recipients}")  # Debug

        # Recréer les cases à cocher
        self.recipient_vars = {}
        for user in recipients.keys():
            var = tk.BooleanVar()
            self.recipient_vars[user] = var
            cb = ttk.Checkbutton(
                self.recipients_list_frame,
                text=user,
                variable=var
            )
            cb.pack(anchor=tk.W, padx=10, pady=2)
        print("Liste des destinataires mise à jour avec succès")  # Debug

    def select_all_recipients(self):
        """Sélectionne tous les destinataires"""
        for var in self.recipient_vars.values():
            var.set(True)

    def deselect_all_recipients(self):
        """Désélectionne tous les destinataires"""
        for var in self.recipient_vars.values():
            var.set(False)

    def add_recipient(self):
        """Ajoute un nouveau destinataire"""
        name = self.new_recipient_name.get().strip()
        chat_id = self.new_recipient_id.get().strip()

        if not name or not chat_id:
            messagebox.showwarning("Attention", "Veuillez remplir tous les champs.")
            return

        try:
            chat_id = int(chat_id)
        except ValueError:
            messagebox.showerror("Erreur", "Le Chat ID doit être un nombre.")
            return

        # Ajouter le destinataire dans la base de données
        if not self.db.add_recipient(name, chat_id):
            messagebox.showwarning("Attention", "Ce nom existe déjà.")
            return

        # Mettre à jour l'interface
        self.update_recipients_list()
        self.new_recipient_name.delete(0, tk.END)
        self.new_recipient_id.delete(0, tk.END)
        messagebox.showinfo("Succès", "Nouveau destinataire ajouté avec succès.")

    def clear_files(self):
        """Efface la liste des fichiers sélectionnés"""
        self.selected_files = []
        self.files_listbox.delete(0, tk.END)
        self.progress_bar['value'] = 0
        self.progress_label['text'] = "Progression : 0%"
        messagebox.showinfo("Info", "La liste des fichiers a été effacée.")

    def select_files(self):
        files = filedialog.askopenfilenames(
            title="Sélectionnez les fichiers à envoyer",
            filetypes=[("Tous les fichiers", "*.*")]
        )
        
        if files:
            self.selected_files = list(files)
            self.files_listbox.delete(0, tk.END)
            for file in self.selected_files:
                self.files_listbox.insert(tk.END, os.path.basename(file))

    async def send_file_to_telegram(self, file_path, chat_id):
        try:
            with open(file_path, 'rb') as file:
                await self.bot.send_document(
                    chat_id=chat_id,
                    document=file,
                    filename=os.path.basename(file_path)
                )
            return True
        except Exception as e:
            print(f"Erreur lors de l'envoi du fichier {file_path}: {str(e)}")
            return False

    def update_progress(self, current, total):
        """Met à jour la barre de progression"""
        percentage = int((current / total) * 100)
        self.progress_bar['value'] = percentage
        self.progress_label['text'] = f"Progression : {percentage}%"
        self.root.update_idletasks()

    def update_history(self):
        """Met à jour l'historique des envois"""
        print("Mise à jour de l'historique...")  # Debug
        # Effacer l'historique actuel
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)

        # Récupérer l'historique depuis la base de données
        history = self.db.get_send_history()
        print(f"Historique récupéré : {history}")  # Debug

        # Ajouter les entrées dans le tableau
        for entry in history:
            recipient_name, file_name, status, sent_at = entry
            self.history_tree.insert('', 'end', values=(sent_at, recipient_name, file_name, status))
        print("Historique mis à jour avec succès")  # Debug

    def send_files(self):
        if not self.selected_files:
            messagebox.showwarning("Attention", "Veuillez sélectionner au moins un fichier.")
            return

        # Récupérer les destinataires sélectionnés
        selected_recipients = [
            user for user, var in self.recipient_vars.items()
            if var.get()
        ]

        if not selected_recipients:
            messagebox.showwarning("Attention", "Veuillez sélectionner au moins un destinataire.")
            return

        async def send_all_files():
            total_files = len(self.selected_files) * len(selected_recipients)
            current_file = 0
            total_success = 0

            recipients = self.db.get_all_recipients()
            for recipient in selected_recipients:
                chat_id = recipients[recipient]
                for file_path in self.selected_files:
                    success = await self.send_file_to_telegram(file_path, chat_id)
                    if success:
                        total_success += 1
                        self.db.log_file_send(recipient, file_path, "Succès")
                    else:
                        self.db.log_file_send(recipient, file_path, "Échec")
                    current_file += 1
                    self.update_progress(current_file, total_files)

            # Mettre à jour l'historique
            self.update_history()
                
            # Message de confirmation avec le nombre total d'envois réussis
            recipients_str = ", ".join(selected_recipients)
            message = f"{total_success}/{total_files} fichiers envoyés avec succès aux destinataires : {recipients_str}"
            messagebox.showinfo("Résultat", message)

        # Réinitialiser la barre de progression
        self.progress_bar['value'] = 0
        self.progress_label['text'] = "Progression : 0%"

        # Créer une nouvelle boucle d'événements asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            # Exécuter la fonction asynchrone
            loop.run_until_complete(send_all_files())
        finally:
            loop.close()

def main():
    print("Démarrage de l'application...")  # Debug
    try:
        # Créer la fenêtre principale
        root = tk.Tk()
        root.withdraw()  # Cacher la fenêtre pendant l'initialisation
        print("Fenêtre principale créée")  # Debug
        
        # Définir la taille minimale de la fenêtre
        root.minsize(800, 600)
        print("Taille minimale définie")  # Debug
        
        # Centrer la fenêtre sur l'écran
        window_width = 800
        window_height = 800
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        print("Fenêtre centrée sur l'écran")  # Debug
        
        # Initialiser l'application
        app = FileSenderApp(root)
        print("Application initialisée avec succès")  # Debug
        
        # Configurer la fermeture de la fenêtre
        def on_closing():
            if messagebox.askokcancel("Quitter", "Voulez-vous vraiment quitter ?"):
                root.quit()
                root.destroy()
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        print("Gestionnaire de fermeture configuré")  # Debug
        
        # Afficher la fenêtre
        root.deiconify()
        root.update()
        print("Fenêtre affichée")  # Debug
        
        # Forcer la fenêtre au premier plan
        root.lift()
        root.attributes('-topmost', True)
        root.after_idle(root.attributes, '-topmost', False)
        print("Fenêtre mise au premier plan")  # Debug
        
        # Configurer un événement périodique pour maintenir la fenêtre active
        def keep_alive():
            root.after(100, keep_alive)
        
        root.after(100, keep_alive)
        print("Keep-alive configuré")  # Debug
        
        print("Démarrage de la boucle principale...")  # Debug
        root.mainloop()
        print("Boucle principale terminée")  # Debug
    except Exception as e:
        print(f"Erreur lors du démarrage de l'application : {str(e)}", file=sys.stderr)  # Debug
        raise

if __name__ == "__main__":
    main()