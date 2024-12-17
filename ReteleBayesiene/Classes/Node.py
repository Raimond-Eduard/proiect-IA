class Node:
    def __init__(self, label, positions, probabilities):
        self.label = label,
        self.positions = positions
        self.probabilites_dict = probabilities

class ChildNode(Node):
    def __init__(self,label, positions, probabilities, parents):
        super().__init__(label, positions, probabilities)
        self.parents = parents
        