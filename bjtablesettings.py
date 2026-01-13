from dataclasses import dataclass
from typing import Optional

@dataclass
class BJTableSettings:
    num_decks: int = 6
    dealer_hits_soft_17: bool = False
    double_after_split: bool = True
    allow_surrender: bool = False
    payout_blackjack: float = 1.5
    insurance_payout: float = 2
    payout: float = 1
    side_bets: Optional[list[str]] = None
    penetration: float = 0.75
    shuffle_point: Optional[int] = None
    cut_card_position: Optional[int] = None
    resplit_aces: bool = False
    max_splits: int = 3
    min_bet: int = 5
    max_bet: int = 500
    table_limits: Optional[list[int]] = None
    continuous_shuffle_machine: bool = False
    num_hands: int = 1