from typing import List
from .card import Card, Rank

class Hand:
    def __init__(self, cards: list[Card] | None = None):
        self._cards = cards if cards is not None else []
        self._value = 0
        self._is_soft = False
        self._dirty = True


    def add_card(self, card: Card):
        self._cards.append(card)
        self._dirty = True


    def split_cards(self) -> Card:
        if len(self._cards) != 2 or self._cards[0].rank != self._cards[1].rank:
            raise ValueError("Can only split a hand with exactly two cards of the same rank.")
        card_to_split = self._cards.pop()
        self._dirty = True
        return card_to_split


    def _recalc(self):
        total = sum(card.value for card in self._cards)
        num_aces = sum(1 for card in self._cards if card.rank == Rank.ACE)

        while num_aces > 0 and total > 21:
            total -= 10
            num_aces -= 1

        self._value = total
        self._is_soft = num_aces > 0
        self._dirty = False


    @property
    def value(self) -> int:
        if self._dirty:
            self._recalc()
        return self._value


    @property
    def is_soft(self) -> bool:
        if self._dirty:
            self._recalc()
        return self._is_soft


    @property
    def cards(self) -> tuple[Card, ...]:
        return tuple(self._cards) 
    

    def __repr__(self) -> str:
        return repr(self.cards)