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

    def __int__(self):
        return self.value * self.color.value

    @staticmethod
    def draw(color: Optional[Color] = None) -> "Card":
        value = random.randrange(1, 11)
        if color is None:
            color = random.randrange(3) % 2
            color = Color.RED if color == 1 else Color.BLACK
        return Card(value, color)