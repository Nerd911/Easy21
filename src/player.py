from .state import State
from .action import Action
from .strategy import Strategy


class Player(object):
    def __init__(self, strategy: Strategy) -> None:
        super().__init__()
        self.strategy = strategy
    
    def take_action(self, state: State) -> Action:
        return self.strategy.take_action(state)

    def update(self, state: State, action: Action, state_prime: State, reward: float) -> None:
        return self.strategy.update(state, action, state_prime, reward)