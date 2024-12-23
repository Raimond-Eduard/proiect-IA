class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Node:
    def __init__(self, label, positions):
        self.label = label
        self.positions = positions
        self.probabilites_dict = None
        self.parents = []

    def set_probabilities(self, probabilities_dict):
        self.probabilites_dict = probabilities_dict

    def set_parent(self, parent):
        self.parents.append(parent)
