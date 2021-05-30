from .card import Card


class State(object):
    def __init__(self, dealer: Card, player: int) -> None:
        super().__init__()
        self.dealer = dealer
        self.player = player

class TerminalState(State):
    def __init__(self, dealer: Card, player: int) -> None:
        super().__init__(dealer, player)