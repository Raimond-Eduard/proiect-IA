class Node:
    def __init__(self, label, positions, probabilities):
        self.label = label
        self.positions = positions
        self.probabilites_dict = probabilities
        self.parents = []
