import tkinter as tk
from tkinter import ttk
import json

class StrategyEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Éditeur de Stratégie")
        self.geometry("1350x800")

        self.blocks = {
            "AX12_Ascenseur": ["initialize_motors", "elevate", "lower", "lower_for_plant"],
            "AX12_Pinces": ["initialize_motors", "open_pince", "open_pince_stepbystep", "close_pince"],
            "AX12_Panneau": ["bouger_panneau_droit", "bouger_panneau_gauche"],
            "ComptagePoints": ["pts_plante_jardiniere", "pts_panneau_solaire", "pts_plante_violet_zone", "pts_zone_finale"],
            "Asserv": []
        }
        self.selected_blocks = []

        self.canvas = tk.Canvas(self, bg="white", width=1200, height=800)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.background_image = tk.PhotoImage(file="FondEditeur.png")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_image)

        self.block_frame = tk.Frame(self, bg="lightgray", padx=10, pady=10)
        self.block_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.block_combobox = ttk.Combobox(self.block_frame, values=list(self.blocks.keys()), font=("Helvetica", 12))
        self.block_combobox.pack(pady=5)
        self.block_combobox.bind("<<ComboboxSelected>>", self.update_method_combobox)

        self.method_combobox = ttk.Combobox(self.block_frame, font=("Helvetica", 12))
        self.method_combobox.pack(pady=5)

        self.argument_label1 = tk.Label(self.block_frame, text="Argument 1:", font=("Helvetica", 12))
        self.argument_label1.pack(pady=5)
        self.argument_entry1 = tk.Entry(self.block_frame, font=("Helvetica", 12))
        self.argument_entry1.pack(pady=5)

        self.argument_label2 = tk.Label(self.block_frame, text="Argument 2:", font=("Helvetica", 12))
        self.argument_label2.pack(pady=5)
        self.argument_entry2 = tk.Entry(self.block_frame, font=("Helvetica", 12))
        self.argument_entry2.pack(pady=5)

        self.add_button = tk.Button(self.block_frame, text="Ajouter", command=self.add_block, font=("Helvetica", 12))
        self.add_button.pack(pady=5)

        self.remove_button = tk.Button(self.block_frame, text="Supprimer", command=self.remove_block, font=("Helvetica", 12))
        self.remove_button.pack(pady=5)

        self.generate_button = tk.Button(self.block_frame, text="Générer JSON", command=self.generate_json, font=("Helvetica", 12))
        self.generate_button.pack(pady=5)

        self.filename_entry = tk.Entry(self.block_frame, font=("Helvetica", 12))
        self.filename_entry.pack(pady=5)

        self.save_button = tk.Button(self.block_frame, text="Enregistrer", command=self.save_json, font=("Helvetica", 12))
        self.save_button.pack(pady=5)

    def update_method_combobox(self, event=None):
        selected_block = self.block_combobox.get()
        methods = self.blocks[selected_block]
        self.method_combobox.config(values=methods)

    def add_block(self):
        block = self.block_combobox.get()
        method = self.method_combobox.get()
        argument1 = self.argument_entry1.get()
        argument2 = self.argument_entry2.get()
        if block == "Asserv":
            self.selected_blocks.append({"classe": block, "methode": method, "argument1": argument1, "argument2": argument2})
        else:
            if not argument1:
                argument1 = None
            if not argument2:
                argument2 = None
            self.selected_blocks.append({"classe": block, "methode": method, "argument1": argument1, "argument2": argument2})
        self.update_canvas()

    def remove_block(self):
        del self.selected_blocks[-1]
        self.update_canvas()

    def update_canvas(self):
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_image)
        for idx, block in enumerate(self.selected_blocks):
            if block['classe'] == "Asserv":
                text = f"{block['classe']} - {block['methode']}({block['argument1']}, {block['argument2']})"
            else:
                args = []
                if block['argument1']:
                    args.append(block['argument1'])
                if block['argument2']:
                    args.append(block['argument2'])
                text = f"{block['classe']} - {block['methode']}({', '.join(args)})"
            self.canvas.create_text(50, (idx + 1) * 30, text=text)

    def generate_json(self):
        json_data = {
            "initialisation": list(self.blocks.keys()),
            "actions": []
        }
        for block in self.selected_blocks:
            data = {
                "classe": block['classe'],
                "methode": block['methode']
            }
            args = []
            if block['argument1'] is not None:
                args.append(block['argument1'])
            if block['argument2'] is not None:
                args.append(block['argument2'])
            data["argument"] = args
            json_data["actions"].append(data)
        self.json_data = json.dumps(json_data, indent=4)

    def save_json(self):
        if hasattr(self, 'json_data'):
            filename = self.filename_entry.get()
            if filename:
                with open(filename, 'w') as f:
                    f.write(self.json_data)
                print("JSON sauvegardé avec succès.")
            else:
                print("Veuillez entrer un nom de fichier.")

if __name__ == "__main__":
    app = StrategyEditor()
    app.mainloop()
