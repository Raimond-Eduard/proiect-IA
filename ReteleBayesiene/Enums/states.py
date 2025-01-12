from enum import Enum


"""
State machines pentru managerierea starile din aplicatie
"""
class StateManager(Enum):
    """
    Clasa de baza pentru state-urile utilizate
    """
    def __eq__(self, other):
        """
        Overload la operatorul egal '==' pentru a verifica daca state-urile apartin
        aceluiasi state machine
        :param other: un alt state
        :return: Boolean
        """
        return isinstance(other, self.__class__) and self.value == other.value

class States(StateManager):
    CREATE = 1
    SOLVE = 2

class CreateStates(StateManager):
    FREE = 0
    CREATE = 1
    ARC = 2
    DELETE = 3
    MODIFY_TABLE = 4


class SolveStates(StateManager):
    FREE = 0
    MAKE_OBSERVATION = 1
    QUERY = 2