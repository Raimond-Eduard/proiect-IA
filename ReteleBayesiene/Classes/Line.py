from Classes.Node import Node

class Line:
    """
    Clasa ce are ca scop usurarea retinerii in memorie a liniilor trasate pe canvas
    """
    def __init__(self, tk_line, start_node, end_node):
        """
        Constructor
        :param tk_line: rezultatul returnat de functia tk.create_line
        :param start_node: obiect de tip nod parinte
        :param end_node: obiect de tip nod copil
        """
        self.line = tk_line
        self.start_node = start_node
        self.end_node = end_node
