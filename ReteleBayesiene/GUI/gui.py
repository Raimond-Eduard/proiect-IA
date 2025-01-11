import tkinter as tk
from logging import setLogRecordFactory
from tkinter import messagebox as msg

from Enums.states import States, CreateStates, SolveStates, CustomGraphs
from GUI.file_actions import FileActions as fa
from GUI.gui_helper_functions import Helper
from Classes.Node import Node, Coord
from Classes.Line import Line
from Classes.EnumerationInference import *

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

        # Dictionar cu nodurile si valorile observate
        self.evidence = {}

        # Array-uri/dictionare de forme, texte si linii pentru stergerea utlerioara
        self.shapes = {}
        self.texts = {}
        self.lines = []

        # Pozitiile mouse-ului pe x si pe y in canvas
        self.mouse_x = None
        self.mouse_y = None

        # Array cu nodurile pentru legarea a 2 noduri
        self.connection = []

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
            command=self.create_new_graph,
            compound=tk.LEFT
        )


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
    def create_new_graph(self):

        self.canvas.delete("all")
        self.state = States.CREATE
        self.shapes = {}
        self.texts = {}
        self.lines = []


    def get_mouse_coords(self, event):
        self.mouse_x = event.x
        self.mouse_y = event.y
        if self.state == States.CREATE and self.create_states == CreateStates.CREATE:
            self.draw_node()

        if self.state == States.CREATE and self.create_states == CreateStates.ARC:
            self.draw_line()

            if len(self.connection) < 2:
                return

            else:
                self.connection = []
        if self.state == States.CREATE and self.create_states == CreateStates.DELETE:
            self.erase_object()

        if self.state == States.CREATE and self.create_states == CreateStates.MODIFY_TABLE:
            self.generate_table()

        if self.state == States.SOLVE and self.solve_states == SolveStates.MAKE_OBSERVATION:
            self.set_output_value_for_clicked_node()

        if self.state == States.SOLVE and self.solve_states == SolveStates.QUERY:
            self.display_query_result()

        self.create_states = CreateStates.FREE
        self.solve_states = SolveStates.FREE
        self.hint_textVariable.set("")

    def display_query_result(self):
        coord = Coord(self.mouse_x, self.mouse_y)
        selected_node = None
        for i in self.node_dict.keys():
            if self.node_dict[i].is_crossing_coords(coord):
                selected_node = self.node_dict[i]
                break

        if selected_node is None:
            return

        temp_network = BayesianNetwork(self.node_dict)
        engine = EnumerationInference(temp_network)

        result = engine.enumeration_ask(selected_node.label, self.evidence)

        top = tk.Toplevel(self)
        top.title("Query result")

        tup = [('Da', result['Da']), ('Nu', result['Nu'])]

        frame_1 = tk.Frame(top)
        frame_2 = tk.Frame(top)

        frame_1.pack()
        frame_2.pack()

        label_1 = tk.Label(frame_1, text=tup[0][0])
        label_2 = tk.Label(frame_1, text=tup[0][1])
        label_3 = tk.Label(frame_1, text=tup[1][0])
        label_4 = tk.Label(frame_1, text=tup[1][1])

        label_1.pack(side=tk.LEFT)
        label_2.pack(side=tk.LEFT)
        label_3.pack(side=tk.LEFT)
        label_4.pack(side=tk.LEFT)

        btn = tk.Button(frame_2, text="Ok", command=top.destroy)
        btn.pack(side=tk.BOTTOM)

    def set_output_value_for_clicked_node(self):

        selected_node = None
        coords = Coord(self.mouse_x, self.mouse_y)
        for i in self.node_dict.keys():
            if self.node_dict[i].is_crossing_coords(coords):
                selected_node =self.node_dict[i]
                break
        if selected_node is None:
            return

        top = tk.Toplevel(self)
        top.title("Observation")
        label = tk.Label(top, text="Set the observed value")
        label.pack()

        listbox = tk.Listbox(top, selectmode=tk.SINGLE)
        listbox.insert(0, "Da")
        listbox.insert(1, "Nu")
        listbox.insert(2, "None")

        listbox.pack()

        btn_1 = tk.Button(top, text="Ok", command=lambda: self.set_observation(listbox, selected_node, top))
        btn_2 = tk.Button(top, text="Cancel", command=top.destroy)

        btn_1.pack()
        btn_2.pack()

    def set_observation(self, listbox, selected_node, top):

        if listbox.curselection() is None:
            msg.showwarning("Warning", "You have to select a value before confirming")
            return

        prev_text = "".join(selected_node.label)
        if 0 in listbox.curselection():

            prev_text = "".join([prev_text, "\nDa"])
            self.evidence[selected_node.label] = 'Da'

        elif 1 in listbox.curselection():

            prev_text = "".join([prev_text, "\nNu"])
            self.evidence[selected_node.label] = 'Nu'

        elif 2 in listbox.curselection():

            if self.evidence[selected_node.label]:
                del self.evidence[selected_node.label]

        self.canvas.itemconfig(self.texts[selected_node.label], text=prev_text)
        top.destroy()


    def generate_table(self):

        coord = Coord(self.mouse_x, self.mouse_y)
        selected_node = None

        for i in list(self.node_dict.keys()):

            if self.node_dict[i].is_crossing_coords(coord):
                selected_node = self.node_dict[i]
                break

        if selected_node is None:
            return

        top = tk.Toplevel(self)
        top.title("Modify probability table")

        labels = []
        inputs = []

        text = selected_node.label
        labels.append(tk.Label(top, text=text).grid(row=0, column=1))
        parents_label_string = "\t"

        if selected_node.parents is not None:
            for i in selected_node.parents:
                parents_label_string += i + "\t"
        row = 1
        labels.append(tk.Label(top, text=parents_label_string).grid(row=row, column=0))
        column = 2
        values = []
        position = 0

        labels.append(tk.Label(top, text="Da").grid(row=1, column=2))
        labels.append(tk.Label(top, text="Nu").grid(row=1, column=3))

        if 'None' in selected_node.probabilities_dict.keys():

            for i in selected_node.probabilities_dict['None'].keys():

                value = selected_node.probabilities_dict['None'][i]
                values.append(tk.StringVar())
                inputs.append(tk.Entry(top, textvariable=values[position]).grid(row=row + 1, column=column))
                values[position].set(str(value))
                position += 1
                column += 1
        else:
            for i in selected_node.probabilities_dict.keys():
                print(selected_node.probabilities_dict.keys())
                print(selected_node.probabilities_dict[i])
                row += 1
                labels.append(tk.Label(top, text=i).grid(row=row, column=0))
                value = selected_node.probabilities_dict[i]['Da']
                values.append(tk.StringVar())
                inputs.append(tk.Entry(top, textvariable=values[position]).grid(row=row, column=2))
                values[position].set(str(value))
                value = selected_node.probabilities_dict[i]['Nu']
                values.append(tk.StringVar())
                values[position + 1].set(str(value))
                inputs.append(tk.Entry(top, textvariable=values[position + 1]).grid(row=row, column=3, padx=5, pady=5))
                position += 2

        button = tk.Button(top, text="Ok", command=lambda: self.set_modified_values(values, selected_node, top))
        cancel = tk.Button(top, text="Cancel", command=top.destroy)
        button.grid(row=row + 2, column=1, pady=10)
        cancel.grid(row=row + 2, column=2, pady=10)

    def set_modified_values(self, modified_values, selected_node, top):

        setter = []
        for i in modified_values:
            setter.append(float(i.get()))

        for i in range(0, len(setter), 2):
            if setter[i] + setter[i + 1] != 1:
                msg.showwarning("Attention", "There is one probability on these rows that is not adding up to 100%.\nCheck and retry.")
                return

        if 'None' in selected_node.probabilities_dict.keys():
            selected_node.probabilities_dict['None']['Da'] = setter[0]
            selected_node.probabilities_dict['None']['Nu'] = setter[1]
        else:

            index = 0

            for i in selected_node.probabilities_dict.keys():
                selected_node.probabilities_dict[i]['Da'] = setter[index]
                selected_node.probabilities_dict[i]['Nu'] = setter[index + 1]
                index += 2
        self.node_dict[selected_node.label].set_probabilities(selected_node.probabilities_dict)
        top.destroy()


    def erase_object(self):

        coord = Coord(self.mouse_x, self.mouse_y)
        for i in list(self.node_dict.keys()):
            if self.node_dict[i].is_crossing_coords(coord):

                self.canvas.delete(self.shapes[i])
                self.canvas.delete(self.texts[i])
                specific_line = None
                for line in self.lines:
                    if self.node_dict[i].label == line.start_node.label or self.node_dict[i] == line.end_node.label:
                        self.canvas.delete(line.line)
                        specific_line = line

                if specific_line is not None:
                    self.lines.remove(specific_line)

                del self.node_dict[i]
                del self.texts[i]
                del self.shapes[i]


    def draw_node(self):
        shape = self.canvas.create_oval(self.mouse_x - 30, self.mouse_y - 30, self.mouse_x + 30, self.mouse_y + 30)
        pop_up = tk.Toplevel(self)
        pop_up.focus_set()
        pop_up.title("Choose a name for the node")
        label = tk.Label(pop_up, text="Name: ")
        value_from_text_box = tk.StringVar(pop_up)

        input_box = tk.Entry(pop_up, textvariable=value_from_text_box)
        input_box.focus()

        label.grid(row=0, column=0, sticky=tk.W, pady=2)
        input_box.grid(row=0, column=1, sticky=tk.W, pady=2)
        exit_button = tk.Button(pop_up, text="OK",
                                command=lambda: self.write_text_on_node(value_from_text_box.get(), pop_up, shape))
        pop_up.bind("<Return>", lambda event: self.write_text_on_node(value_from_text_box.get(), pop_up, shape))
        exit_button.grid(row=1, sticky=tk.S)

    def write_text_on_node(self, text, pop_up, shape):
        text_bound = self.canvas.create_text(self.mouse_x, self.mouse_y, text=text)
        self.node_dict[text] = Node(text, Coord(self.mouse_x, self.mouse_y))
        default_probability = {'None': {'Da': 0.5, 'Nu': 0.5}}
        self.node_dict[text].set_probabilities(default_probability)
        self.shapes[text] = shape
        self.texts[text] = text_bound

        pop_up.destroy()

    def draw_network_after_loading_from_file(self):

        for i in self.node_dict.keys():

            x = self.node_dict[i].coordinates.x
            y = self.node_dict[i].coordinates.y
            self.shapes[i] = self.canvas.create_oval(x - 30, y - 30, x + 30, y + 30)

            label = self.node_dict[i].label
            self.texts[i] = self.canvas.create_text(x, y, text=label)

            if self.node_dict[i].parents is not None:

                parents = self.node_dict[i].parents

                for parent in parents:
                    line = self.canvas.create_line(self.node_dict[parent].coordinates.x, self.node_dict[parent].coordinates.y,
                                                   self.node_dict[i].coordinates.x, self.node_dict[i].coordinates.y, arrow=tk.LAST)
                    self.lines.append(Line(line, self.node_dict[parent], self.node_dict[i]))


    def draw_line(self):
        coord = Coord(self.mouse_x, self.mouse_y)
        for i in self.node_dict.keys():
            if self.node_dict[i].is_crossing_coords(coord):
                if not self.connection:
                    self.node_dict[i].define_as_parent()
                self.connection.append(self.node_dict[i])

        if len(self.connection) == 2:
            parent_tag = self.connection[0].label
            child_tag = self.connection[1].label

            self.node_dict[child_tag].set_parents(parent_tag)
            new_dict = {}
            tup = ('Da', 'Nu')
            if 'None' in self.node_dict[child_tag].probabilities_dict.keys():

                for i in tup:
                    new_dict[i] = {'Da': 0.5, 'Nu': 0.5}

                self.node_dict[child_tag].set_probabilities(new_dict)
            else:
                new_dict = {}
                for prob in self.node_dict[child_tag].probabilities_dict.keys():
                    for i in tup:
                        new_label = prob + ', ' + i
                        new_dict[new_label] = {'Da': 0.5, 'Nu': 0.5}

                self.node_dict[child_tag].set_probabilities(new_dict)

            position_1 = self.connection[0].coordinates
            position_2 = self.connection[1].coordinates

            line = self.canvas.create_line(position_1.x, position_1.y, position_2.x, position_2.y, arrow=tk.LAST)
            self.lines.append(Line(line, self.node_dict[parent_tag], self.node_dict[child_tag]))

    def open_custom_sample(self):
        top = tk.Toplevel(self)
        top.geometry("720x240")
        top.title("Custom Graph")

        listbox = tk.Listbox(top, width=40, height=10, selectmode=tk.SINGLE)

        listbox.insert(1, "Problema Febrei")

        btn = tk.Button(top, text='Load Selection', command=lambda: self.load_selected_graphs(listbox, top))
        btn.pack(side='bottom')
        listbox.pack()

    def load_selected_graphs(self, listbox, pop_up):

        file = {}

        for i in listbox.curselection():
            if i == CustomGraphs.FEVER_PROBLEM.value:
                file = Helper.return_parsed_json("../defaults/Problema_Febrei.json")
            # Aici vor mai aparea retele, teoretic aici ar fi un switch dar in python nu avem switch

        pop_up.destroy()

        self.create_network_after_loading_from_file(file)

    def create_network_after_loading_from_file(self, json_dictionary):
        for i in json_dictionary.keys():
            x = json_dictionary[i]['position']['x']
            y = json_dictionary[i]['position']['y']
            self.node_dict[i] = Node(i, Coord(x, y))
            parents = json_dictionary[i]['parents']
            if parents is not None:
                for j in parents:
                    self.node_dict[i].set_parents(j)
            probability_dict = json_dictionary[i]['prob']
            final_prob_dict = {}

            for label, probabilities in probability_dict.items():
                label = ', '.join(label) if label else 'None'
                final_prob_dict[label] = {}

                for outcome, probability in probabilities.items():
                    final_prob_dict[label][outcome] = probability
            self.node_dict[i].set_probabilities(final_prob_dict)
        self.draw_network_after_loading_from_file()


    def set_create_frame(self):
        '''
        Functie care se ocupa de modificarea dinamica a frame-ului
        cu butoane in cazul in care starea este pe create
        :return: void
        '''
        tk.Button(self.actions_frame, text="Create", command=self.create_node).pack(pady=5, padx=10, side=tk.LEFT, anchor=tk.NW)
        tk.Button(self.actions_frame, text="Create Arc", command=self.create_arc).pack(pady=5, padx=10, side=tk.LEFT, anchor=tk.NW)
        tk.Button(self.actions_frame, text="Delete", command=self.delete_object).pack(pady=5, padx=10, side=tk.LEFT, anchor=tk.NW)
        tk.Button(self.actions_frame, text="Modify probability table", command=self.modify_probability_table).pack(pady=5, padx=10, side=tk.LEFT, anchor=tk.NW)
        # Trebuie adaugate alte butoane

    def modify_probability_table(self):

        self.create_states = CreateStates.MODIFY_TABLE

        if len(self.node_dict) == 0:
            msg.showwarning("Attention", "Insert nodes first")
            return

        self.hint_textVariable.set("Click on an existing node to modify it\'s probability table")

    def delete_object(self):

        self.create_states = CreateStates.DELETE
        if len(self.node_dict) == 0:
            msg.showwarning("Attention", "You have nothing drawn in order for you to delete...")
            return

        self.hint_textVariable.set("Click on an existing node to delete it with it and it\'s properties")

    def create_arc(self):

        self.create_states = CreateStates.ARC

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
        tk.Button(self.actions_frame, text="Make Observation", command=self.make_observation).pack(pady=5, padx=10, side=tk.LEFT, anchor=tk.NW)
        tk.Button(self.actions_frame, text="Query", command=self.make_query).pack(pady=5, padx=10, side=tk.LEFT, anchor=tk.NW)

    def make_query(self):
        if len(self.node_dict) == 0:
            msg.showwarning("Attention", "You have nothing drawn in order for you to query")
            return
        self.solve_states = SolveStates.QUERY
        self.hint_textVariable.set("Click on the canvas below to make a query")

    def make_observation(self):

        if len(self.node_dict) == 0:
            msg.showwarning("Attention", "Insert nodes first")
            return

        self.solve_states = SolveStates.MAKE_OBSERVATION
        self.hint_textVariable.set("Click on an existing node to specify it's output value")



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