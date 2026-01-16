from typing import Protocol
from enum import Enum

class PlayMove(Enum):
    HIT = "H"
    STAND = "S"
    DOUBLE = "D"
    DOUBLE_STAND = "DS"
    SPLIT = "SP"
    SPLIT_IF_DAS = "SPD"
    SURRENDER_HIT = "RH"
    SURRENDER_STAND = "RS"

class PlayStrategy(Protocol):
    def get_move(self, player_cards, dealer_upcard) -> PlayMove: ...