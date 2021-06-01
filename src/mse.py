from typing import Dict, Tuple
from .state import State
from .card import Card, Color
from .action import Action

def mse(Q0:Dict[Tuple[State, Action], float], Q1: Dict[Tuple[State, Action], float]) -> float:
    res = 0.0
    for i in range(1, 11):
        for j in range(0, 22):
            for action in [Action.HIT, Action.STICK]:
                state = State(Card(i, Color.BLACK), j)
                v0 = Q0[(state, action)]
                v1 = Q1[(state, action)]
#                 print(str(state))
#                 print(f"v0 {v0}")
#                 print(f"v1 {v1}")

                res += (v0 - v1)**2
    return res**0.5
