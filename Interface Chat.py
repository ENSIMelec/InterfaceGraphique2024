import tkinter as tk

class TeamSelectionPage(tk.Frame):
    def __init__(self, parent, on_team_selected):
        super().__init__(parent)

        self.on_team_selected = on_team_selected

        self.configure(bg="white")
        self.pack(fill=tk.BOTH, expand=True)

        # Création de la fenêtre principale
        self.left_frame = tk.Frame(self, bg="#FFFF99", width=500, height=667, bd=2, relief="groove")  # Equipe Jaune
        self.left_frame.grid(row=0, column=0, sticky="nsew")

        self.right_frame = tk.Frame(self, bg="#000080", width=500, height=667, bd=2, relief="groove")  # Equipe Bleue
        self.right_frame.grid(row=0, column=1, sticky="nsew")

        # Création des boutons pour la sélection de l'équipe
        self.yellow_team_button = tk.Button(self.left_frame, text="Equipe Jaune", font=("Helvetica", 14, "bold"), command=self.select_yellow_team, bd=2, relief="groove")
        self.yellow_team_button.place(relx=0.5, rely=0.5, anchor="center")

        self.blue_team_button = tk.Button(self.right_frame, text="Equipe Bleue", font=("Helvetica", 14, "bold"), command=self.select_blue_team, bd=2, relief="groove")
        self.blue_team_button.place(relx=0.5, rely=0.5, anchor="center")

    def select_yellow_team(self):
        self.on_team_selected("Equipe Jaune")

    def select_blue_team(self):
        self.on_team_selected("Equipe Bleue")

class StrategySelectionPage(tk.Frame):
    def __init__(self, parent, team, return_callback, show_steps_selection):
        super().__init__(parent)

        self.team = team
        self.return_callback = return_callback
        self.show_steps_selection = show_steps_selection

        self.configure(bg="white")
        self.pack(fill=tk.BOTH, expand=True)

        # Chargement de l'image
        image_path = "vinyle_table_2024_FINAL_V1.png"
        self.image = tk.PhotoImage(file=image_path)

        # Création du cadre pour le premier bloc avec l'image en arrière-plan
        self.frame_with_image = tk.Frame(self, bg="white", width=1000, height=667, bd=2, relief="groove")  # Fond blanc
        self.frame_with_image.pack(fill=tk.BOTH, expand=True)

        # Affichage de l'image en arrière-plan
        self.background_label = tk.Label(self.frame_with_image, image=self.image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Création du cadre pour les boutons
        self.frame_with_buttons = tk.Frame(self.frame_with_image, bg="#000080", bd=2, relief="groove")  # Bleu marine
        if self.team == "Equipe Jaune":
            self.frame_with_buttons.place(relx=0.05, rely=0.2, relwidth=0.4, relheight=0.7)
            button_color = "#FFFF99"  # Jaune clair
            return_button_side = "right"
            selected_button_color = "#FFD700"  # Jaune foncé
        elif self.team == "Equipe Bleue":
            self.frame_with_buttons.place(relx=0.55, rely=0.2, relwidth=0.4, relheight=0.7)
            button_color = "#99CCFF"  # Bleu pastel
            return_button_side = "left"
            selected_button_color = "#00008B"  # Bleu foncé

        # Création du titre de l'équipe sélectionnée
        team_color = "#FFFF99" if self.team == "Equipe Jaune" else "#99CCFF"
        self.team_title_label = tk.Label(self.frame_with_buttons, text=self.team, font=("Helvetica", 24, "bold"), bg=team_color)
        self.team_title_label.pack(fill=tk.BOTH, padx=10, pady=5)

        # Création des boutons de sélection de stratégie
        self.buttons = []
        for i in range(1, 5):
            button = tk.Button(self.frame_with_buttons, text=f"Stratégie N°{i}", font=("Helvetica", 12, "bold"), command=lambda strategy_number=i: self.on_strategy_selected(strategy_number), bd=2, relief="groove")
            button.configure(bg=button_color)  # Pas de bordure
            button.pack(fill="both", expand=True, padx=10, pady=5)
            self.buttons.append(button)

        # Création du bouton de retour à la page de sélection d'équipe
        self.return_button = tk.Button(self.frame_with_buttons, text="Retour à la sélection d'équipe", font=("Helvetica", 12), bg="#FFDDC1", command=self.return_callback, bd=2, relief="groove")
        self.return_button.pack(side=return_button_side, fill=tk.BOTH, padx=10, pady=5)

    def on_strategy_selected(self, strategy_number):
        self.pack_forget()
        self.show_steps_selection()

class StepsSelectionPage(tk.Frame):
    def __init__(self, parent, return_callback):
        super().__init__(parent)

        self.return_callback = return_callback

        self.configure(bg="white")
        self.pack(fill=tk.BOTH, expand=True)

        # Chargement de l'image
        image_path = "vinyle_table_2024_FINAL_V1.png"
        self.image = tk.PhotoImage(file=image_path)

        # Création du cadre pour le premier bloc avec l'image en arrière-plan
        self.frame_with_image = tk.Frame(self, bg="white", width=1000, height=667, bd=2, relief="groove")  # Fond blanc
        self.frame_with_image.pack(fill=tk.BOTH, expand=True)

        # Affichage de l'image en arrière-plan
        self.background_label = tk.Label(self.frame_with_image, image=self.image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Création du cadre pour la succession des étapes
        self.steps_frame = tk.Frame(self.frame_with_image, bg="#000080", bd=2, relief="groove")
        self.steps_frame.place(relx=0.25, rely=0.2, relwidth=0.5, relheight=0.7)  # Centrer horizontalement

        # Création des cases Étape N°X (les étapes de la stratégie)
        self.step_labels = []
        for i in range(1, 11):
            step_label = tk.Label(self.steps_frame, text=f"Étape N°{i}", font=("Helvetica", 14, "bold"), bg="#FFFF99", bd=2, relief="groove")
            step_label.bind("<Button-1>", self.on_drag_start)
            step_label.pack(fill="both", padx=10, pady=5)
            self.step_labels.append(step_label)

        # Création du bouton de retour à la page de sélection de stratégie
        self.return_button = tk.Button(self.frame_with_image, text="Retour à la sélection de stratégie", font=("Helvetica", 12), bg="#FFDDC1", command=self.return_callback, bd=2, relief="groove")
        self.return_button.place(relx=0.7, rely=0.9, anchor="center")

        # Variables pour le déplacement
        self.drag_data = {"x": 0, "y": 0, "item": None}

    def on_drag_start(self, event):
        widget = event.widget
        self.drag_data["item"] = widget
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def on_drag_motion(self, event):
        x = self.winfo_pointerx() - self.winfo_rootx() - self.drag_data["x"]
        y = self.winfo_pointery() - self.winfo_rooty() - self.drag_data["y"]
        self.drag_data["item"].place(x=x, y=y)

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Interface Graphique")
        self.geometry("1000x667")

        self.team_selection_page = TeamSelectionPage(self, self.on_team_selected)

    def on_team_selected(self, team):
        self.team_selection_page.pack_forget()
        self.strategy_selection_page = StrategySelectionPage(self, team, self.return_to_team_selection, self.show_steps_selection)

    def return_to_team_selection(self):
        self.strategy_selection_page.destroy()
        self.team_selection_page.pack(fill=tk.BOTH, expand=True)

    def show_steps_selection(self):
        self.steps_selection_page = StepsSelectionPage(self, self.return_to_strategy_selection)
        self.strategy_selection_page.pack_forget()

    def return_to_strategy_selection(self):
        self.steps_selection_page.destroy()
        self.strategy_selection_page.pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
