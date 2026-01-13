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
    ACE   = 11
    JACK  = 12
    QUEEN = 13
    KING  = 14

    @property
    def value(self):
        if self in (Rank.JACK, Rank.QUEEN, Rank.KING):
            return 10
        if self == Rank.ACE:
            return 11
        return self._value_

class Suit(Enum):
    SPADES   = "S"
    HEARTS   = "H"
    DIAMONDS = "D"
    CLUBS    = "C"
    
@dataclass(frozen=True)
class Card:
    rank: Rank
    suit: Suit

    SUIT_SYMBOLS = {
        Suit.SPADES: "♠",
        Suit.HEARTS: "♥",
        Suit.DIAMONDS: "♦",
        Suit.CLUBS: "♣"
    }

    RANK_DISPLAY = {
        Rank.ACE: "A",
        Rank.JACK: "J",
        Rank.QUEEN: "Q",
        Rank.KING: "K",
    }

    for r in Rank:
        if r not in RANK_DISPLAY:
            RANK_DISPLAY[r] = str(r.value)

    @property
    def value(self) -> int:
        return self.rank.value
    
    def __repr__(self) -> str:
        return f"{self.RANK_DISPLAY[self.rank]}{self.SUIT_SYMBOLS[self.suit]}"