from hashlib import new
from .state import State, TerminalState
from .action import Action
from typing import Tuple
from .card import Card
Reward = int

def step(state: State, action: Action) -> Tuple[State, Reward]:
    assert not  isinstance(state, TerminalState)
    assert not state.player < 1
    assert not state.player > 21
    if action == Action.HIT:
        new_card = Card.draw()
        new_player = state.player + int(new_card)
        if new_player < 1 or new_player > 21:
            res = TerminalState(state.dealer, new_player)
            return (res, -1)
        res = State(state.dealer, new_player)
        return (res, 0)

    dealer_sum = int(state.dealer)
    new_card = state.dealer
    while dealer_sum > 1 and dealer_sum < 17:
        new_card = Card.draw()
        dealer_sum += int(new_card)
    res = TerminalState(new_card, state.player)
    if dealer_sum < 1 or dealer_sum > 21 or dealer_sum < state.player:
        return (res, 1)
    if dealer_sum == state.player:
        return (res, 0)
    return (res, -1)
