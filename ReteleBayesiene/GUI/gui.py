import tkinter as tk

from Classes.states import StateManager, States
from GUI.file_actions import FileActions as fa


class GUI(tk.Tk):
    def __init__(self, state=States.CREATE):
        super().__init__()

        # Initializare state machine (create sau solve)
        self.state = StateManager()

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

        # Frame pentru switch-ul dintre create si solve
        self.state_frame = tk.Frame(self, bg="lightgray", padx=15, pady=15)
        self.state_frame.pack(fill="x")

        # Atasarea butoanelor de create si solve
        self.create_button = tk.Button(self.state_frame, text="Create", command=lambda: self.switch_states(States.CREATE))
        self.create_button.pack(side="left", padx=10)

        self.solve_button = tk.Button(self.state_frame, text="Solve", command=lambda: self.switch_states(States.SOLVE))
        self.solve_button.pack(side="left", padx=10)

        # Interfata va porni in mod default pe CREATE, asadar butonul create va fi dimmed
        self.create_button.config(state=tk.DISABLED)

        '''
        Urmeaza frame-ul in care se vor schimba actiunile in functie de mod
        Modul Create: Va avea butoane care sa creeze noduri
        Modul Solve: Va avea butoane care tine de interogarea nodurilor.
        '''
        self.actions_frame = tk.Frame(self, bg="white", padx=5, pady=5, relief="ridge", borderwidth=2)
        self.actions_frame.pack(fill="both", expand=True, pady=10, side=tk.TOP, anchor=tk.NW)

        self.set_create_frame()

        # Frame-ul in care se va situa canvasul
        self.canvas_frame = tk.Frame(self, bg="lightgrey", padx=5, pady=5)
        self.canvas_frame.pack(fill="both", expand=True, pady=10, side=tk.TOP, anchor=tk.NW)

        # Canvasul propriu-zis
        self.canvas = tk.Canvas(self.canvas_frame, bg="white", width=1920, height=1080)
        self.canvas.pack(side="left", fill="y")

        # Scrollbar
        self.scrollbar = tk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.h_scrollbar = tk.Scrollbar(self.canvas_frame, orient="horizontal", command=self.canvas.xview)
        self.h_scrollbar.pack(side="bottom", fill="x")

        self.canvas.configure(yscrollcommand=self.scrollbar.set, xscrollcommand=self.h_scrollbar.set)

        # Linie de testat canvas, va fi stearsa mai tarziu
        self.line = self.canvas.create_line(20, 50, 1900, 800, fill="red")

    def set_create_frame(self):
        '''
        Functie care se ocupa de modificarea dinamica a frame-ului
        cu butoane in cazul in care starea este pe create
        :return: void
        '''
        tk.Button(self.actions_frame, text="Create").pack(pady=5, padx=10, side=tk.LEFT, anchor=tk.NW)
        tk.Button(self.actions_frame, text="Select").pack(pady=5, padx=10, side=tk.LEFT, anchor=tk.NW)
        # Trebuie adaugate alte butoane

    def set_solve_frame(self):
        '''
        Functie care se ocupa de modificare a frame-ului
        la state-ul de tip solve
        :return: void
        '''
        tk.Button(self.actions_frame, text="Make Observation").pack(pady=5, padx=10, side=tk.LEFT, anchor=tk.NW)
        tk.Button(self.actions_frame, text="Query").pack(pady=5, padx=10, side=tk.LEFT, anchor=tk.NW)

    def switch_states(self,state):

        self.state.__setstate__(state)

        for widget in self.actions_frame.winfo_children():
            widget.destroy()

        if state == States.CREATE:

            self.create_button.config(state=tk.DISABLED)
            self.solve_button.config(state=tk.NORMAL)

            self.set_create_frame()

        elif state == States.SOLVE:

            self.solve_button.config(state=tk.DISABLED)
            self.create_button.config(state=tk.NORMAL)
            self.set_solve_frame()


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
    print("This is supposed to be just the interface, the main program is ran in main.py")
    gui = GUI()
    gui.mainloop()