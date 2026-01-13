from typing import List
from models.card import Card, Rank

class PlayerHand:
    def __init__(self, cards: List[Card] = [], bet: int = 0):
        self.cards = cards
        self.bet = bet
        self.value = 0
        self.soft_value = False

        if cards:
            self._recalculate_value()
    
    def add_card(self, card: Card):
        self.cards.append(card)
        self._recalculate_value()
    
    def _recalculate_value(self):
        total = sum(card.value for card in self.cards)
        num_aces = sum(1 for card in self.cards if card.rank == Rank.ACE)
        
        while num_aces > 0 and total > 21:
            total -= 10
            num_aces -= 1
        
        self.value = total
        self.soft_value = num_aces > 0

    def __repr__(self) -> str:
        return repr(self.cards)