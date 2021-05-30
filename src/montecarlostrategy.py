from .state import State, TerminalState
from .action import Action
from .strategy import Strategy
from collections import defaultdict
import random

class MonteCarloStrategy(Strategy):
    def __init__(self, N_0: int = 100):
        self.N_0 = N_0
        self.N = defaultdict(lambda: 0)
        self.V = defaultdict(lambda: 0.0)
        self.Q = defaultdict(lambda: 0.0)
        self.episode = []
        self.epsilon = lambda s: self.N_0 / (self.N_0 + self.N[s])
        self.alpha = lambda s, a: 1.0 / self.N[(s, a)]

    def take_action(self, state: State) -> Action:
        eps = self.epsilon(state)
        if random.random() < eps:
            action = random.choice([Action.HIT, Action.STICK])
        else:
            action = Action.HIT if self.Q[(state, Action.HIT)] > self.Q[(state, Action.STICK)] else Action.STICK
        return action

    def update(self, state: State, action: Action, state_prime: State, reward: float) -> None:
        self.N[(state)] += 1
        self.N[(state, action)] += 1
        self.episode.append((state, action, reward))
        if not isinstance(state_prime, TerminalState):
            return
        G = sum([sar[-1] for sar in self.episode])
        for state, action, _ in self.episode:
            self.Q[(state, action)] += self.alpha(state, action) * (G - self.Q[(state, action)])
        self.episode = []