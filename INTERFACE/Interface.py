import tkinter as tk
import os
import shutil
import subprocess

import logging
import logging.config

# Dynamic font size adjustment based on window dimensions
def get_font_size(width, height, base_size=20):
    # Calculate size based on smaller dimension
    size = int(min(width, height) / 800 * base_size)
    return max(size, 12)  # Minimum font size of 12

class TeamSelectionPage(tk.Frame):
    def __init__(self, parent, on_team_selected):
        
        super().__init__(parent)

        self.logger = parent.logger

        self.on_team_selected = on_team_selected

        self.configure(bg="white")
        self.pack(fill=tk.BOTH, expand=True)

        # Set grid weight to make the layout responsive
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Dynamic frames using relative sizes
        self.left_frame = tk.Frame(self, bg="#FFFF99", bd=2, relief="groove")  # Equipe Jaune
        self.left_frame.grid(row=0, column=0, sticky="nsew")

        self.right_frame = tk.Frame(self, bg="#000080", bd=2, relief="groove")  # Equipe Bleue
        self.right_frame.grid(row=0, column=1, sticky="nsew")

        # Dynamic font size and button placement
        font_size = get_font_size(self.winfo_width(), self.winfo_height())
        self.yellow_team_button = tk.Button(self.left_frame, text="Equipe Jaune",
                                            font=("Helvetica", font_size, "bold"),
                                            command=lambda: self.select_team("Jaune"),
                                            bd=2, relief="groove")
        self.yellow_team_button.place(relx=0.5, rely=0.5, anchor="center")

        self.blue_team_button = tk.Button(self.right_frame, text="Equipe Bleue",
                                          font=("Helvetica", font_size, "bold"),
                                          command=lambda: self.select_team("Bleue"),
                                          bd=2, relief="groove")
        self.blue_team_button.place(relx=0.5, rely=0.5, anchor="center")

        self.logger.info("Fin intitialisation TeamSelectionPage")

    def select_team(self, team):
        self.logger.info(f"Equipe sélectionnée: {team}")  
        self.on_team_selected(team)

class StrategySelectionPage(tk.Frame):
    def __init__(self, parent, team, return_callback, show_steps_selection):
        super().__init__(parent)
        
        self.logger = parent.logger

        self.team = team
        self.return_callback = return_callback
        self.show_steps_selection = show_steps_selection

        self.configure(bg="white")
        self.pack(fill=tk.BOTH, expand=True)

        # Chargement de l'image
        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(script_dir, "/home/pi/code_principal_2024/InterfaceGraphique2024/INTERFACE/vinyle_table_2024_FINAL_v1.png")
        self.image = tk.PhotoImage(file=image_path)

        # Création du cadre pour le premier bloc avec l'image en arrière-plan
        self.frame_with_image = tk.Frame(self, bg="black", width=800, height=480, bd=2, relief="groove")  # Fond blanc
        self.frame_with_image.pack(fill=tk.BOTH, expand=True)

        # Affichage de l'image en arrière-plan
        self.background_label = tk.Label(self.frame_with_image, image=self.image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Création du cadre pour les boutons
        self.frame_with_buttons = tk.Frame(self.frame_with_image, bd=2, relief="groove")  # Bleu marine
        if self.team == "Jaune":
            self.frame_with_buttons.configure(bg="#FFFF99")
            self.frame_with_buttons.place(relx=0.05, rely=0.2, relwidth=0.4, relheight=0.7)
            button_color = "#FFFF99"  # Jaune clair
            return_button_side = "right"
            selected_button_color = "#FFD700"  # Jaune foncé
        elif self.team == "Bleue":
            self.frame_with_buttons.configure(bg="#000080")
            self.frame_with_buttons.place(relx=0.55, rely=0.2, relwidth=0.4, relheight=0.7)
            button_color = "#99CCFF"  # Bleu pastel
            return_button_side = "left"
            selected_button_color = "#00008B"  # Bleu foncé

        # Création du titre de l'équipe sélectionnée
        self.team_title_label = tk.Label(self.frame_with_buttons, text=self.team, font=("Helvetica", 30, "bold"), bg=button_color)
        self.team_title_label.pack(fill=tk.BOTH, padx=15, pady=7)

        self.buttons = []

        self.strategy_files = os.listdir('/home/pi/code_principal_2024/Stratégies/')
        # Création des boutons de sélection de stratégie
        for strategy_file in self.strategy_files:
            button_text = f"{strategy_file[:-5]}"
            button = tk.Button(self.frame_with_buttons, text=button_text, font=("Helvetica", 15, "bold"), command=lambda strategy_file=strategy_file: self.on_strategy_selected(strategy_file), bd=2, relief="groove")
            button.configure(bg=button_color)  # Pas de bordure
            button.pack(fill="both", expand=True, padx=20, pady=5)
            self.buttons.append(button)
       
        # Création du bouton de retour à la page de sélection d'équipe  
        self.return_button = tk.Button(self.frame_with_buttons, text="Retour à la sélection d'équipe", font=("Helvetica", 15), bg="#FFDDC1", command=self.return_callback, bd=2, relief="groove")

        self.return_button.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.logger.info("Fin initialisation StrategySelectionPage")

    def on_strategy_selected(self, strategy_number):
        json_filename = f"/home/pi/code_principal_2024/Stratégies/{strategy_number}"
        self.logger.info(f"Stratégie sélectionnée: {json_filename} en couleur {self.team}")
        # Copie du fichier JSON dans le dossier STRATEGIE
        shutil.copy(json_filename, "/home/pi/code_principal_2024/InterfaceGraphique2024/INTERFACE/STRATEGIE/STRATEGIE.json")
        self.pack_forget()
        self.show_steps_selection(1)

class StepsSelectionPage(tk.Frame):
    def __init__(self, parent, strategy_number, return_callback):
        super().__init__(parent)
        
        self.logger = parent.logger

        self.strategy_number = strategy_number
        self.return_callback = return_callback
        self.program_running = False  # Indicateur pour suivre l'état d'exécution du programme

        self.configure(bg="white")
        self.pack(fill=tk.BOTH, expand=True)

        # Chargement de l'image
        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(script_dir, "/home/pi/code_principal_2024/InterfaceGraphique2024/INTERFACE/fond_ENSIMelec.png")
        self.image = tk.PhotoImage(file=image_path)

        # Création du cadre pour le premier bloc avec l'image en arrière-plan
        self.frame_with_image = tk.Frame(self, bg="black", width=800, height=480, bd=2, relief="groove")  # Fond blanc
        self.frame_with_image.pack(fill=tk.BOTH, expand=True)

        # Affichage de l'image en arrière-plan
        self.background_label = tk.Label(self.frame_with_image, image=self.image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Création du bloc pour le nombre de points
        self.points_block = tk.Frame(self.frame_with_image, bg="#7AC5CD", bd=2, relief="groove")  # Rouge pâle
        self.points_block.place(relx=0.425, rely=0.2325, relwidth=0.15, relheight=0.26)

        # Titre du bloc
        self.points_label = tk.Label(self.points_block, text="Points", font=("Helvetica", 23, "bold"), bg="#FCFCFC")
        self.points_label.pack(fill=tk.BOTH, padx=10, pady=5)

        # Variable pour stocker le nombre de points
        self.points_counter_value = tk.StringVar()
        points_mapping = {1: 57, 2: 2, 3: 3, 4: 4}
        self.points_counter_value.set(str(points_mapping.get(strategy_number, 0)))  # Initialisation à 0

        # Compteur initialisé à 0
        self.points_counter = tk.Label(self.points_block, textvariable=self.points_counter_value, font=("Helvetica", 50), bg="#FCFCFC")
        self.points_counter.pack(fill=tk.BOTH, padx=10, pady=5)

        # Création du bouton GO pour exécuter le programme
        self.go_button = tk.Button(self.frame_with_image, text="GO", font=("Helvetica", 30), bg="#BCEE68", command=self.run_program, bd=2, relief="groove")
        self.go_button.place(relx=0.82, rely=0.20, anchor="center")

        # Création du bouton STOP pour fermer le programme
        self.stop_button = tk.Button(self.frame_with_image, text="STOP", font=("Helvetica", 17), bg="#FF6347", command=self.stop_program, bd=2, relief="groove")
        self.stop_button.place(relx=0.82, rely=0.36, anchor="center")

        # Création de l'indicateur visuel de l'état d'exécution
        self.status_indicator = tk.Label(self.frame_with_image, text="Programme arrêté", font=("Helvetica", 20), bg="red", fg="black")
        self.status_indicator.place(relx=0.82, rely=0.48, anchor="center")

        # Création du bouton de retour à la page de sélection de stratégie
        self.return_button = tk.Button(self.frame_with_image, text="Retour à la sélection de stratégie", font=("Helvetica", 13), bg="#FFDDC1", command=self.return_callback, bd=2, relief="groove")
        self.return_button.place(relx=0.22, rely=0.36, anchor="center")

        self.process = None

        self.logger.info("Fin initialisation StepsSelectionPage")

    def run_program(self):
        if not self.program_running:
            # Exécute le programme externe (vous devez spécifier le chemin d'accès correct)
            self.logger.info("Lancement du programme principal")
            self.process = subprocess.Popen(["python", "/home/pi/code_principal_2024/main_code.py"])
            self.program_running = True
            self.status_indicator.config(text="Programme en cours", bg="#BCEE68")
            # Désactiver le bouton de retour
            self.return_button.config(state=tk.DISABLED)


    def stop_program(self):
        if self.program_running:
            self.logger.info("Arrêt du programme principal")
            # Arrête le programme externe
            if self.process is not None:  # Vérifiez si un processus est en cours d'exécution
                self.process.terminate()  # Arrêtez le processus
                self.process = None  # Réinitialisez l'objet processus
            self.program_running = False
            self.status_indicator.config(text="Programme arrêté", bg="red")
            # Réactiver le bouton de retour
            self.return_button.config(state=tk.NORMAL)

class MainApplication(tk.Tk):
    def __init__(self):
        # Charger la configuration de logging
        logging.config.fileConfig("/home/pi/code_principal_2024/logs.conf")

        # Créer un logger
        self.logger = logging.getLogger("Interface")
        super().__init__()

        self.title("Interface Graphique")
        self.geometry("800x480")
        self.after(1000, lambda: self.wm_attributes('-fullscreen', 'true'))
        self.logger.info("Début initialisation TeamSelectionPage")
        self.team_selection_page = TeamSelectionPage(self, self.on_team_selected)
        self.logger.info("Fin initialisation MainApplication")

    def on_team_selected(self, team):
        self.team_selection_page.pack_forget()
        self.strategy_selection_page = StrategySelectionPage(self, team, self.return_to_team_selection, self.show_steps_selection)

    def return_to_team_selection(self):
        self.logger.info("Retour à la sélection d'équipe")
        self.strategy_selection_page.destroy()
        self.team_selection_page.pack(fill=tk.BOTH, expand=True)

    def show_steps_selection(self, strategy_number):
        self.steps_selection_page = StepsSelectionPage(self, strategy_number, self.return_to_strategy_selection)
        self.strategy_selection_page.pack_forget()

    def return_to_strategy_selection(self):
        self.logger.info("Retour à la sélection de stratégie")
        # Suppression du fichier JSON copié dans le dossier STRATEGIE
        if os.path.exists("/home/pi/code_principal_2024/InterfaceGraphique2024/INTERFACE/STRATEGIE/STRATEGIE.json"):  # Vérifier si le fichier existe
            os.remove("/home/pi/code_principal_2024/InterfaceGraphique2024/INTERFACE/STRATEGIE/STRATEGIE.json")  # Supprimer le fichier
        self.steps_selection_page.destroy()
        self.strategy_selection_page.pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
