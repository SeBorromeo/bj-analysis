from dataclasses import dataclass
from enum import Enum

class Rank(Enum):
    TWO   = 2
    THREE = 3
    FOUR  = 4
    FIVE  = 5
    SIX   = 6
    SEVEN = 7
    EIGHT = 8
    NINE  = 9
    TEN   = 10
    JACK  = 10
    QUEEN = 10
    KING  = 10
    ACE   = 11   # soft value

class Suit(Enum):
    SPADES   = "S"
    HEARTS   = "H"
    DIAMONDS = "D"
    CLUBS    = "C"
    
@dataclass(frozen=True)
class Card:
    rank: Rank
    suit: Suit

    @property
    def value(self) -> int:
        return self.rank.value