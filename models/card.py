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
    
    def __repr__(self) -> str:
        suit_symbols = {
            Suit.SPADES: "♠",
            Suit.HEARTS: "♥",
            Suit.DIAMONDS: "♦",
            Suit.CLUBS: "♣"
        }
        rank_display = {
            Rank.ACE: "A",
            Rank.KING: "K",
            Rank.QUEEN: "Q",
            Rank.JACK: "J",
            **{r: str(r.value) for r in Rank if r.value <= 10}
        }
        return f"{rank_display[self.rank]}{suit_symbols[self.suit]}"