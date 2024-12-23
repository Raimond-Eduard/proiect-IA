import tkinter as tk
from tkinter import messagebox as msg

from Enums.states import States, CreateStates, SolveStates
from GUI.file_actions import FileActions as fa
from GUI.gui_helper_functions import Helper
from Classes.Node import Node, Coord

class GUI(tk.Tk):
    def __init__(self, state=States.CREATE):
        super().__init__()

        # Aici sunt variabile de stare ale interfetei
        # Prima este un dictionar cu string-uri ce are ca scop afisarea de indicii
        # in interfata pentru utilizator ca sa inteleaga ce actiune este activa la momentul respectiv
        self.helper_text = {
            "Create" : "Create mode: Click on the canvas below to create a node",
            "Select" : "Select mode: Click on a node to select it and change properties",
            "Make Observation" : "Make Observation mode: Click on a node to specify if it has a specific value before querying",
            "Query" : "Query mode: Click on a node to query it\'s probability"
        }

        # Dictionar de noduri cu referinte
        self.node_dict = {}
        # Pozitiile mouse-ului pe x si pe y in canvas
        self.mouse_x = None
        self.mouse_y = None

        # Initializare state machine
        self.state = States.CREATE
        self.create_states = CreateStates.FREE
        self.solve_states = SolveStates.FREE

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
            command=self.open_custom_sample, # TO DO - open custom sample
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

        # Text label care indica hint-uri catre utilizator
        self.hint_textVariable = tk.StringVar()
        self.hint_textVariable.set("")

        self.hint_label = tk.Label(self.state_frame, textvariable=self.hint_textVariable)
        self.hint_label.pack(side="right", padx=10)


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
        self.canvas.bind("<Button-1>", self.get_mouse_coords)

        # Scrollbar
        self.scrollbar = tk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.h_scrollbar = tk.Scrollbar(self.canvas_frame, orient="horizontal", command=self.canvas.xview)
        self.h_scrollbar.pack(side="bottom", fill="x")

        self.canvas.configure(yscrollcommand=self.scrollbar.set, xscrollcommand=self.h_scrollbar.set)


        # Linie de testat canvas, va fi stearsa mai tarziu
        # self.line = self.canvas.create_line(20, 50, 1900, 800, fill="red")

    def get_mouse_coords(self, event):
        self.mouse_x = event.x
        self.mouse_y = event.y
        if self.state == States.CREATE and self.create_states == CreateStates.CREATE:
            self.canvas.create_oval(self.mouse_x - 30, self.mouse_y - 30, self.mouse_x + 30, self.mouse_y + 30)
            pop_up = tk.Toplevel(self)
            pop_up.title("Choose a name for the node")
            label = tk.Label(pop_up, text="Name: ")
            value_from_text_box = tk.StringVar(pop_up)

            input_box = tk.Entry(pop_up, textvariable=value_from_text_box)

            label.grid(row=0, column=0, sticky=tk.W, pady=2)
            input_box.grid(row=0, column=1, sticky=tk.W, pady=2)

            exit_button = tk.Button(pop_up, text="OK", command=lambda: self.write_text_on_node(value_from_text_box.get(), pop_up))
            exit_button.grid(row=1, sticky=tk.S)

        self.create_states = CreateStates.FREE
        self.hint_textVariable.set("")

    def write_text_on_node(self, text, pop_up):
        self.canvas.create_text(self.mouse_x, self.mouse_y, text=text)
        self.node_dict[text] = Node(text, Coord(self.mouse_x, self.mouse_y))
        pop_up.destroy()


    def open_custom_sample(self):
        top = tk.Toplevel(self)
        top.geometry("720x240")
        top.title("Custom Graph")

        listbox = tk.Listbox(top, width=40, height=10, selectmode=tk.SINGLE)

        listbox.insert(1, "Problema Febrei")

        btn = tk.Button(top, text='Load Selection', command=lambda: Helper.get_selected_value(listbox))
        btn.pack(side='bottom')
        listbox.pack()

    def set_create_frame(self):
        '''
        Functie care se ocupa de modificarea dinamica a frame-ului
        cu butoane in cazul in care starea este pe create
        :return: void
        '''
        tk.Button(self.actions_frame, text="Create", command=self.create_node).pack(pady=5, padx=10, side=tk.LEFT, anchor=tk.NW)
        tk.Button(self.actions_frame, text="Select").pack(pady=5, padx=10, side=tk.LEFT, anchor=tk.NW)
        tk.Button(self.actions_frame, text="Create Arc", command=self.create_arc).pack(pady=5, padx=10, side=tk.LEFT, anchor=tk.NW)
        # Trebuie adaugate alte butoane

    def create_arc(self):
        if len(self.node_dict) < 2:
            msg.showwarning("Attention", "There are not enough nodes to create an arc between them")
            return

        self.hint_textVariable.set("Click on a node, then on another node to create a connection between them\n"
                                   "The first node is going to be a parent for the second node")


    def create_node(self):
        self.hint_textVariable.set("Click on the canvas below to create a node")
        self.create_states = CreateStates.CREATE
        # TO DO: Adaugarea logicii si a altor actiuni in starea asta

    def set_solve_frame(self):
        '''
        Functie care se ocupa de modificare a frame-ului
        la state-ul de tip solve
        :return: void
        '''
        tk.Button(self.actions_frame, text="Make Observation").pack(pady=5, padx=10, side=tk.LEFT, anchor=tk.NW)
        tk.Button(self.actions_frame, text="Query").pack(pady=5, padx=10, side=tk.LEFT, anchor=tk.NW)



    def switch_states(self,state):

        self.state = state

        for widget in self.actions_frame.winfo_children():
            widget.destroy()


        if self.state == States.CREATE:

            self.create_button.config(state=tk.DISABLED)
            self.solve_button.config(state=tk.NORMAL)

            self.set_create_frame()

        elif self.state == States.SOLVE:

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