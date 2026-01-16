from typing import Protocol
from bj_sim.game.models.card import Card

class CountingStrategy(Protocol):
    def get_tag(self, card: Card) -> int: ...
