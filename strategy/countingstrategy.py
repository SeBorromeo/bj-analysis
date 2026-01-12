from typing import Protocol
from models.card import Card

class CountingStrategy(Protocol):
    def get_tag(self, card: Card) -> int: ...
