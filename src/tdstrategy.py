from .state import State, TerminalState
from .action import Action
from .strategy import Strategy
from collections import defaultdict
import random

class TDStrategy(Strategy):
    def __init__(self, N_0: int = 100,  lam: float = 0.1):
        self.N_0 = N_0
        self.N = defaultdict(lambda: 0)
        self.E = defaultdict(lambda: 0.0)
        self.Q = defaultdict(lambda: 0.0)
        self.episode = []
        self.epsilon = lambda s: self.N_0 / (self.N_0 + self.N[s])
        self.alpha = lambda s, a: 1.0 / self.N[(s, a)]
        self.lam = lam

    def take_action(self, state: State) -> Action:
        eps = self.epsilon(state)
        if random.random() < eps:
            action = random.choice([Action.HIT, Action.STICK])
        else:
            action = Action.HIT if self.Q[(state, Action.HIT)] > self.Q[(state, Action.STICK)] else Action.STICK
        return action

    def _update(self, state: State, action: Action, td_error: float) -> None:
        self.N[(state, action)] += 1
        self.E[(state, action)] += 1
        for state, action, _ in self.episode:
            self.Q[(state, action)] += self.alpha(state, action) * td_error * self.E[(state, action)]
            self.E[(state, action)] *= self.lam

    def update(self, state: State, action: Action, state_prime: State, reward: float) -> None:
        if len(self.episode) == 0:
            self.episode.append((state, action, reward))
            return
        last_state, last_action, last_reward = self.episode[-1]
        td_error = last_reward - self.Q[(last_state, last_action)] + self.Q[(state, action)]
        self._update(last_state, last_action, td_error)
        self.episode.append((state, action, reward))
        if not isinstance(state_prime, TerminalState):
            return
        last_state, last_action, last_reward = self.episode[-1]
        td_error = last_reward - self.Q[(last_state, last_action)]
        self._update(last_state, last_action, td_error)
        self.episode = []