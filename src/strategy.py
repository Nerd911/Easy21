from .state import State
from .action import Action

class Strategy(object):
    def take_action(self, state: State) -> Action:
        return Action.STICK

    def update(self, state: State, action: Action, state_prim: State) -> None:
        pass