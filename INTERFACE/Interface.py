import tkinter as tk
import os
import sys
sys.path.append('/home/pi/code_principal_2024')
from Main import *
from Globals_Variables import *

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

    def on_strategy_selected(self, strategy_path):
        json_filename = f"/home/pi/code_principal_2024/Stratégies/{strategy_path}"
        self.logger.info(f"Stratégie sélectionnée: {json_filename} en couleur {self.team}")
        self.pack_forget()
        self.show_steps_selection(json_filename)

class StepsSelectionPage(tk.Frame):
    def __init__(self, parent, strategy_path, return_callback):
        super().__init__(parent)
        
        self.logger = parent.logger

        self.strategy_path = strategy_path
        self.return_callback = return_callback
        self.main = MainCode(json_path=strategy_path, app=self)

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
        self.points_block = tk.Frame(self.frame_with_image, bg="#7AC5CD", bd=2, relief="groove")
        self.points_block.place(relx=0.5, rely=0.05, relwidth=0.2, relheight=0.1, anchor="n")

        # Titre du bloc
        self.points_label = tk.Label(self.points_block, text="Points", font=("Helvetica", 23, "bold"), bg="#FCFCFC")
        self.points_label.pack(fill=tk.BOTH, padx=10, pady=5)

        # Variable pour stocker le nombre de points
        self.points_counter_value = tk.StringVar()
        self.points_counter_value.set('57')  # Initialisation à 0

        # Compteur initialisé à 0
        self.points_counter = tk.Label(self.points_block, textvariable=self.points_counter_value, font=("Helvetica", 50), bg="#FCFCFC")
        self.points_counter.pack(fill=tk.BOTH, padx=10, pady=5)

        # Current Action Display
        self.current_action_label = tk.Label(self.frame_with_image, text="Aucune action en cours", font=("Helvetica", 16), bg="white")
        self.current_action_label.place(relx=0.5, rely=0.16, anchor="n")

        # Initialization Indicators
        self.init_indicators = tk.Frame(self.frame_with_image, bg="#222", relief="flat")
        self.init_indicators.place(relx=0.5, rely=0.9, anchor="s", relwidth=1, height=30)
        
        # List of components
        components = ["Asserv", "Lidar", "Ascenseur", "Panneau", "Pinces"]
        self.indicators = {}
        for i, component in enumerate(components):
            self.indicators[component] = tk.Label(self.init_indicators, text=component, font=("Helvetica", 12), bg="red", fg="white", bd=2, relief="groove")
            self.indicators[component].pack(side="left", expand=True, fill="both")
        
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
        self.return_button = tk.Button(self.frame_with_image, text="Return to Strategy Selection", font=("Helvetica", 13), bg="#FFDDC1", command=self.return_callback, bd=2, relief="groove")
        self.return_button.place(relx=0.5, rely=0.16, anchor="n")

        self.X_label = tk.Label(self.frame_with_image, text="X: 0", font=("Helvetica", 16), bg="white")
        self.X_label.place(relx=0.3, rely=0.16, anchor="n")
        self.Y_label = tk.Label(self.frame_with_image, text="Y: 0", font=("Helvetica", 16), bg="white")
        self.Y_label.place(relx=0.7, rely=0.16, anchor="n")

        # Désactiver le bouton stop
        self.stop_button.config(state=tk.DISABLED)

        self.logger.info("Fin initialisation StepsSelectionPage")

    def run_program(self):
        # Exécute le programme externe (vous devez spécifier le chemin d'accès correct)
        self.logger.info("Lancement du programme principal")
        self.main.run()

    def stop_program(self):
        self.logger.info("Arrêt du programme principal")
        self.main.stop()

    def retour(self):
        self.logger.info("Retour à la sélection de stratégie")
        self.return_callback

    def mainStart(self):
        # Activer le bouton de stop
        self.stop_button.config(state=tk.NORMAL)
        print("IIIIIIIIH")
        # Désactiver le bouton de retour
        self.return_button.config(state=tk.DISABLED)
        print("OOOOOH")
        # Désactiver le bouton de start
        self.go_button.config(state=tk.DISABLED)
        print("AAAAAH")
        self.status_indicator.config(text="Programme en cours...", bg="green")
        
    def mainStop(self):
        # Réactiver le bouton de retour
        self.return_button.config(state=tk.NORMAL)
        # Résactiver le bouton de start
        self.go_button.config(state=tk.NORMAL)
        # Désactiver le bouton de stop
        self.stop_button.config(state=tk.DISABLED)
        self.status_indicator.config(text="Programme arrêté", bg="red")

    def waiting_jack(self):
        self.frame_with_image.config(bg="red")
        tk.Label(self.frame_with_image, text="Waiting Jack...", font=("Helvetica", 30), bg="red", fg="white").pack(expand=True)

    def jack_retired(self):
        label = tk.Label(self.frame_with_image, text="Jack Retired", font=("Helvetica", 30), bg="green", fg="white")
        label.pack(expand=True)

    def update_current_action(self, action):
        self.current_action_label.config(text=action)

    def initialize_component(self, component_name):
        if component_name in self.indicators:
            self.indicators[component_name].config(bg="green")

    def asserv_initialized(self):
        self.initialize_component("Asserv")

    def lidar_initialized(self):
        self.initialize_component("Lidar")

    def AX12_Ascenceur_initialized(self):
        self.initialize_component("Ascenseur")

    def AX12_Panneau_initialized(self):
        self.initialize_component("Panneau")

    def AX12_Pinces_initialized(self):
        self.initialize_component("Pinces")

    def update_score(self,score):
        self.points_counter_value.set(str(score))

    def X_update(self, X):
        self.X_label.config(text=f"X: {X}")

    def Y_update(self, Y):
        self.Y_label.config(text=f"Y: {Y}")

    def time_update(self, time):
        pass

class MainApplication(tk.Tk):
    def __init__(self):
        # Charger la configuration de logging
        logging.config.fileConfig(LOGS_CONF_PATH)

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

    def show_steps_selection(self, strategy_path):
        self.steps_selection_page = StepsSelectionPage(self, strategy_path, self.return_to_strategy_selection)
        self.strategy_selection_page.pack_forget()

    def return_to_strategy_selection(self):
        self.logger.info("Retour à la sélection de stratégie")
        self.steps_selection_page.destroy()
        self.strategy_selection_page.pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
