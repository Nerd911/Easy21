import random
import enum
from typing import Optional

class Color(enum.Enum):
    RED = -1
    BLACK = 1

class Card(object):
    def __init__(self, value: int, color: Color) -> None:
        super().__init__()
        self.value = value
        self.color = color

    def __int__(self) -> int:
        return self.value * self.color.value

    def __eq__(self, other: "Card") -> bool:
        return self.value == other.value and self.color == other.color

    def __hash__(self) -> int:
        return hash((self.value, self.color))

    def __str__(self) -> str:
        return f"Card: {self.color.name} {self.value}"

    @staticmethod
    def draw(color: Optional[Color] = None) -> "Card":
        value = random.randrange(1, 11)
        if color is None:
            color = random.randrange(3) % 2
            color = Color.RED if color == 1 else Color.BLACK
        return Card(value, color)