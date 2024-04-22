import tkinter as tk
import os
import shutil

class TeamSelectionPage(tk.Frame):
    def __init__(self, parent, on_team_selected):
        super().__init__(parent)

        self.on_team_selected = on_team_selected

        self.configure(bg="white")
        self.pack(fill=tk.BOTH, expand=True)

        # Création de la fenêtre principale
        self.left_frame = tk.Frame(self, bg="#FFFF99", width=990, height=1080, bd=2, relief="groove")  # Equipe Jaune
        self.left_frame.grid(row=0, column=0, sticky="nsew")

        self.right_frame = tk.Frame(self, bg="#000080", width=990, height=1080, bd=2, relief="groove")  # Equipe Bleue
        self.right_frame.grid(row=0, column=1, sticky="nsew")

        # Création des boutons pour la sélection de l'équipe
        self.yellow_team_button = tk.Button(self.left_frame, text="Equipe Jaune", font=("Helvetica", 40, "bold"), command=lambda: self.select_team("Jaune"), bd=2, relief="groove")
        self.yellow_team_button.place(relx=0.5, rely=0.5, anchor="center")

        self.blue_team_button = tk.Button(self.right_frame, text="Equipe Bleue", font=("Helvetica", 40, "bold"), command=lambda: self.select_team("Bleue"), bd=2, relief="groove")
        self.blue_team_button.place(relx=0.5, rely=0.5, anchor="center")

    def select_team(self, team):
        self.on_team_selected(team)

class StrategySelectionPage(tk.Frame):
    def __init__(self, parent, team, return_callback, show_steps_selection):
        super().__init__(parent)

        self.team = team
        self.return_callback = return_callback
        self.show_steps_selection = show_steps_selection

        self.configure(bg="white")
        self.pack(fill=tk.BOTH, expand=True)

        # Chargement de l'image
        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(script_dir, "vinyle_table_2024_FINAL_v1.png")
        self.image = tk.PhotoImage(file=image_path)

        # Création du cadre pour le premier bloc avec l'image en arrière-plan
        self.frame_with_image = tk.Frame(self, bg="black", width=1980, height=1080, bd=2, relief="groove")  # Fond blanc
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
        self.team_title_label = tk.Label(self.frame_with_buttons, text=self.team, font=("Helvetica", 36, "bold"), bg=button_color)
        self.team_title_label.pack(fill=tk.BOTH, padx=20, pady=10)

        # Création des boutons de sélection de stratégie
        self.buttons = []
        for i in range(1, 5):
            button_text = f"Stratégie N°{i}"
            if self.team == "Jaune" and i == 1:
                button_text = "Stratégie N°1 (MODIFIÉE)"
            elif self.team == "Bleue" and i == 1:
                button_text = "Stratégie N°1 (MODIFIÉE)"
            button = tk.Button(self.frame_with_buttons, text=button_text, font=("Helvetica", 24, "bold"), command=lambda strategy_number=i: self.on_strategy_selected(strategy_number), bd=2, relief="groove")
            button.configure(bg=button_color)  # Pas de bordure
            button.pack(fill="both", expand=True, padx=20, pady=10)
            self.buttons.append(button)

        # Création du bouton de retour à la page de sélection d'équipe
        self.return_button = tk.Button(self.frame_with_buttons, text="Retour à la sélection d'équipe", font=("Helvetica", 24), bg="#FFDDC1", command=self.return_callback, bd=2, relief="groove")
        self.return_button.pack(side=return_button_side, fill=tk.BOTH, padx=20, pady=10)

    def on_strategy_selected(self, strategy_number):
        json_filename = f"Stratégie N°{strategy_number} {self.team}.json"
        # Copie du fichier JSON dans le dossier STRATEGIE
        shutil.copy(json_filename, "STRATEGIE")
        self.pack_forget()
        self.show_steps_selection(strategy_number)

class StepsSelectionPage(tk.Frame):
    def __init__(self, parent, strategy_number, return_callback):
        super().__init__(parent)

        self.strategy_number = strategy_number
        self.return_callback = return_callback

        self.configure(bg="white")
        self.pack(fill=tk.BOTH, expand=True)

        # Chargement de l'image
        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(script_dir, "fond_ENSIMelec.png")
        self.image = tk.PhotoImage(file=image_path)

        # Création du cadre pour le premier bloc avec l'image en arrière-plan
        self.frame_with_image = tk.Frame(self, bg="black", width=1980, height=1080, bd=2, relief="groove")  # Fond blanc
        self.frame_with_image.pack(fill=tk.BOTH, expand=True)

        # Affichage de l'image en arrière-plan
        self.background_label = tk.Label(self.frame_with_image, image=self.image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Création du bloc pour le nombre de points
        self.points_block = tk.Frame(self.frame_with_image, bg="#7AC5CD", bd=2, relief="groove")  # Rouge pâle
        self.points_block.place(relx=0.425, rely=0.21, relwidth=0.15, relheight=0.28)

        # Titre du bloc
        self.points_label = tk.Label(self.points_block, text="Points", font=("Helvetica", 60, "bold"), bg="#FCFCFC")
        self.points_label.pack(fill=tk.BOTH, padx=10, pady=5)

        # Variable pour stocker le nombre de points
        self.points_counter_value = tk.StringVar()
        points_mapping = {1: 57, 2: 2, 3: 3, 4: 4}
        self.points_counter_value.set(str(points_mapping.get(strategy_number, 0)))  # Initialisation à 0

        # Compteur initialisé à 0
        self.points_counter = tk.Label(self.points_block, textvariable=self.points_counter_value, font=("Helvetica", 150), bg="#FCFCFC")
        self.points_counter.pack(fill=tk.BOTH, padx=10, pady=5)

        # Création du bouton de retour à la page de sélection de stratégie
        self.return_button = tk.Button(self.frame_with_image, text="Retour à la sélection de stratégie", font=("Helvetica", 28), bg="#FFDDC1", command=self.return_callback, bd=2, relief="groove")
        self.return_button.place(relx=0.78, rely=0.17, anchor="center")

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Interface Graphique")
        self.attributes('-fullscreen', True)  # Lancement en plein écran

        self.team_selection_page = TeamSelectionPage(self, self.on_team_selected)

    def on_team_selected(self, team):
        self.team_selection_page.pack_forget()
        self.strategy_selection_page = StrategySelectionPage(self, team, self.return_to_team_selection, self.show_steps_selection)

    def return_to_team_selection(self):
        # Suppression du fichier JSON copié dans le dossier STRATEGIE
        if os.path.exists("STRATEGIE"):
            shutil.rmtree("STRATEGIE")
        self.strategy_selection_page.destroy()
        self.team_selection_page.pack(fill=tk.BOTH, expand=True)

    def show_steps_selection(self, strategy_number):
        self.steps_selection_page = StepsSelectionPage(self, strategy_number, self.return_to_strategy_selection)
        self.strategy_selection_page.pack_forget()

    def return_to_strategy_selection(self):
        # Suppression du dossier STRATEGIE et son contenu
        if os.path.exists("STRATEGIE"):
            shutil.rmtree("STRATEGIE")
        self.steps_selection_page.destroy()
        self.strategy_selection_page.pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
