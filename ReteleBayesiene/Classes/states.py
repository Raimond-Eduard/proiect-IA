from enum import Enum

class States(Enum):
    CREATE = 1
    SOLVE = 2

class StateManager:
    def __init__(self, state=States.CREATE):
        self.state = state

    def __getstate__(self):
        return self.state

    def __setstate__(self, state):
        if state not in [States.CREATE, States.SOLVE]:
            raise Exception("Invalid state, somehow you managed to insert a 3rd state")
        self.state = state