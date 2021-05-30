from .card import Card, Color

class State(object):
    def __init__(self, dealer: Card, player: int) -> None:
        super().__init__()
        self.dealer = dealer
        self.player = player
    
    @staticmethod
    def init() -> "State":
        dealer = Card.draw(Color.BLACK)
        player = int(Card.draw(Color.BLACK))
        return State(dealer, player)
    
    def __str__(self) -> str:
        return f"State: Player - {self.player}, Dealer - {self.dealer}"

    def __eq__(self, other: "State") -> bool:
        return self.dealer == other.dealer and self.player == other.player

    def __hash__(self) -> int:
        return hash((self.dealer, self.player))

class TerminalState(State):
    def __init__(self, dealer: Card, player: int) -> None:
        super().__init__(dealer, player)