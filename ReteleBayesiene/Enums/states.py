from enum import Enum

class StateManager(Enum):
    def __eq__(self, other):
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

class CustomGraphs(StateManager):
    FEVER_PROBLEM = 0