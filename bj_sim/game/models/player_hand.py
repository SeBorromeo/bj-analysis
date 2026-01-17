from typing import List
from .card import Card, Rank
from .hand import Hand

class PlayerHand(Hand):
    def __init__(self, cards: List[Card] = [], bet: int = 0):
        super().__init__(cards)
        self._bet = bet
        self._surrender = False
        self._hasDoubled = False


    def double_bet(self):
        if not self._hasDoubled:
            self._hasDoubled = True
            self._bet *= 2
        else:
            raise ValueError("Cannot double bet more than once per hand.")


    def surrender_hand(self):
        self._surrender = True
    

    @property
    def bet(self) -> int:
        return self._bet


    @property
    def surrender(self) -> bool:
        return self._surrender
    
        