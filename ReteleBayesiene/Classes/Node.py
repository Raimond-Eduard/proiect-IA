class Coord:
    """
    Clasa ce ajuta la stocarea coordonatelor
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        """
        Supraincarcare operatorului de egalitate '==' pentru egalitatea intre 2 obiecte
        :param other: un alt obiect de tip Coord
        :return: Boolean
        """
        return self.x == other.x and self.y == other.y

    def __str__(self):
        """
        Adaugarea metodei str pentru a converti obiectul la string
        :return: String
        """
        return f"X: {self.x}, Y: {self.y}"

    def __repr__(self):
        """
        Acelasi lucru doar ca pentru print-uri
        :return: String
        """
        return f"X: {self.x}, Y: {self.y}"


class Node:
    """
    Clasa ce detine toata logica nodurilor
    """
    def __init__(self, label, positions):
        """
        Constructor ce seteaza majoritatea valorilor pe None
        :param label: String - Titlul nodului
        :param positions: Coord - Coordonatele la care se afla nodul
        """
        self.label = label
        self.probabilities_dict = None
        self.parents = []
        self.coordinates = positions
        self.is_parent = None
        self.output = None
    """
    Din nou functiile str si repr dezvoltate pentru debug
    """
    def __str__(self):
        return f"Label: {self.label}, Probabilities: {self.probabilities_dict}, Parents: {self.parents}, coordinates: {self.coordinates}"

    def __repr__(self):
        return f"Label: {self.label}, Probabilities: {self.probabilities_dict}, Parents: {self.parents}, coordinates: {self.coordinates}"

    def set_probabilities(self, probabilities_dict):
        """
        Seteaza dictionarul de probabilitati
        :param probabilities_dict: Dictionarul de probabilitati procesat
        :return:
        """
        self.probabilities_dict = probabilities_dict

    def set_parents(self, parent):
        """
        Seteaza lista de parinti
        :param parent: Node
        :return: None
        """
        if parent in self.parents:
            return

        self.parents.append(parent)

    def define_as_parent(self):
        """
        Seteaza nodul ca parinte
        :return:
        """
        self.is_parent = True

    def set_coordinates(self, x, y):
        """
        Schimbarea coordonatelor in caz de orice
        :param x: Integer - coordonata pe x
        :param y: Integer - coordonata pe y
        :return:void
        """
        self.coordinates = Coord(x,y)

    def is_crossing_other_node(self, collided):
        """
        Verificare daca 2 noduri se intersecteaza
        :param collided: Alt nod
        :return: Boolean
        """
        return collided.coordinates.x - 30 <= self.coordinates.x <= collided.coordinates.x + 30 and \
            collided.coordinates.y - 30 <= self.coordinates.y <= collided.coordinates.y +30

    def is_crossing_coords(self, coord):
        """
        Verificare daca coordonatele se afla pe un nod
        :param coord: Coord
        :return: Boolean
        """
        return self.coordinates.x - 30 <= coord.x <= self.coordinates.x + 30 and \
            self.coordinates.y - 30 <= coord.y <= self.coordinates.y + 30