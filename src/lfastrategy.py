from typing import List
from .state import State, TerminalState
from .action import Action
from .strategy import Strategy
from collections import defaultdict
import random
import numpy as np

class LFAStrategy(Strategy):
    def __init__(self, N_0: int = 100,  lam: float = 0.1, epsilon=0.05, alpha=0.01, features=None, feature_len=None):
        if not features:
            self.features = self.create_features()
            self.feature_len = 36
        else:
            self.features = features
            assert feature_len
            self.feature_len = feature_len
        self.N_0 = N_0
        self.N = [0 for _ in range(self.feature_len)]
        self.E = [0.0 for _ in range(self.feature_len)]
        self.Q = defaultdict(lambda: 0.0)
        self.episode = []
        self.epsilon = epsilon
        self.alpha = alpha
        self.lam = lam
        self.theta = np.random.randn(self.feature_len)

    def take_action(self, state: State) -> Action:
        eps = self.epsilon
        if random.random() < eps:
            action = random.choice([Action.HIT, Action.STICK])
        else:
            action = Action.HIT if self.get_q(state, Action.HIT) > self.get_q(state, Action.STICK) else Action.STICK
        return action

    def _update(self, state: State, action: Action, td_error: float) -> None:
        ids_to_update = self.lookup_features(state, action)
        for idx in ids_to_update:
            self.N[idx] += 1
            self.E[idx] += 1
            for state, action, _ in self.episode:
                self.theta[idx] += self.alpha * td_error * self.E[idx]
                self.E[idx] *= self.lam
        self.Q[(state, action)] = self.get_q(state, action)

    def update(self, state: State, action: Action, state_prime: State, reward: float) -> None:
        if len(self.episode) == 0:
            self.episode.append((state, action, reward))
            return
        last_state, last_action, last_reward = self.episode[-1]
        td_error = last_reward - self.get_q(last_state, last_action) + self.get_q(state, action)
        self._update(last_state, last_action, td_error)
        self.episode.append((state, action, reward))
        if not isinstance(state_prime, TerminalState):
            return
        last_state, last_action, last_reward = self.episode[-1]
        td_error = last_reward - self.get_q(last_state, last_action)
        self._update(last_state, last_action, td_error)
        self.episode = []

    def create_features(self) -> List:
        dealer = [(1, 4), (4, 7), (7, 10)]
        player = [(1, 6), (4, 9), (7, 12), (10, 15), (13, 18), (16, 21)]
        actions = [Action.HIT, Action.STICK]
        features = []
        for d in dealer:
            for p in player:
                for a in actions:
                    features.append((p, d, a))
        return features

    def lookup_features(self, state: State, action: Action) -> List:
        player, dealer = state.player, int(state.dealer)
        ids_to_update = []
        for i, (p, d, a) in enumerate(self.features):
            if p[0] <= player <= p[1] and d[0] <= dealer <= d[1] and a == action:
                ids_to_update.append(i)
        return ids_to_update

    def get_q(self, state, action):
        ids_to_update = self.lookup_features(state, action)
        q_value = 0
        for idx in ids_to_update:
            q_value += self.theta[idx]
        return q_value

