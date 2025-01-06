class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"X: {self.x}, Y: {self.y}"

    def __repr__(self):
        return f"X: {self.x}, Y: {self.y}"


class Node:
    def __init__(self, label, positions):
        self.label = label
        self.probabilities_dict = None
        self.parents = []
        self.coordinates = positions
        self.is_parent = None
        self.output = None

    def __str__(self):
        return f"Label: {self.label}, Probabilities: {self.probabilities_dict}, Parents: {self.parents}, coordinates: {self.coordinates}"

    def __repr__(self):
        return f"Label: {self.label}, Probabilities: {self.probabilities_dict}, Parents: {self.parents}, coordinates: {self.coordinates}"

    def set_probabilities(self, probabilities_dict):

        self.probabilities_dict = probabilities_dict

    def set_parents(self, parent):

        if parent in self.parents:
            return

        self.parents.append(parent)

    def define_as_parent(self):

        self.is_parent = True

    def set_coordinates(self, x, y):

        self.coordinates = Coord(x,y)

    def is_crossing_other_node(self, collided):

        return collided.coordinates.x - 30 <= self.coordinates.x <= collided.coordinates.x + 30 and \
            collided.coordinates.y - 30 <= self.coordinates.y <= collided.coordinates.y +30

    def is_crossing_coords(self, coord):

        return self.coordinates.x - 30 <= coord.x <= self.coordinates.x + 30 and \
            self.coordinates.y - 30 <= coord.y <= self.coordinates.y + 30

    def set_output(self, value):

        if value not in [True, False]:
            raise Exception("Invalid value provided")

        self.output = value