import sys
import tkinter as tk
from file_actions import FileActions as fa

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()

        # Initializarea dimensiunilor si titlului
        self.geometry("1240x640")
        self.title("Inferente prin enumerare in retele bayesiene")


        # Generarea unui meniu in partea de sus a interfetei
        self.menubar = tk.Menu()
        self.file_menu = tk.Menu(self.menubar, tearoff=False)

        # Butonul file + comenzi
        self.file_menu.add_command(
            label="New Graph",
            accelerator="Ctrl+N",
            command=fa.create_new_graph,
            compound=tk.LEFT
        )

        # Comenzi de pe butonul file
        self.bind("<Control-n>", fa.create_new_graph)
        self.bind("<Control-N>", fa.create_new_graph)

        # Speram sa avem timp sa implementam si asta
        self.file_menu.add_command(
            label="Load Custom Graph",
            command=fa.open_custom_sample,
            compound=tk.LEFT
        )

        self.file_menu.add_command(
            label="Load From File",
            command=fa.open_file,
            compound=tk.LEFT
        )

        self.file_menu.add_separator()
        self.file_menu.add_command(
            label="Save",
            accelerator="Ctrl+S",
            command=fa.save_file,
            compound=tk.LEFT
        )

        self.bind("<Control-s>", fa.save_file)
        self.bind("<Control-S>", fa.save_file)

        self.file_menu.add_command(
            label="Exit",
            command=self.destroy,
            compound=tk.LEFT
        )

        # Comenzi pentru meniul help
        self.help_menu = tk.Menu(self.menubar, tearoff=False)

        self.help_menu.add_command(
            label="About",
            compound=tk.LEFT,
            command=self.display_about
        )

        # Adaugarea in bara a meniului 'File'
        self.menubar.add_cascade(menu=self.file_menu, label="File")
        self.menubar.add_cascade(menu=self.help_menu, label="Help")
        self.config(menu=self.menubar)

    def display_about(self):
        top = tk.Toplevel(self)
        top.geometry("720x240")
        top.title("About")
        (tk.Label(top, text="This app uses the Bayesian inference algorithm to "
                           "display a way of computing decision models based on "
                           "given probabilities\n"
                           + "\u00A9" +
                 "2024 Sinziana Maieczki & Raimond Butnaru - Artificial Inteligence project")
         .place(x=0,y=50))

if __name__ == "__main__":
    gui = GUI()
    gui.mainloop()