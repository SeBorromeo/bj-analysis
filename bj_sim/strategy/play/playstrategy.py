from typing import Protocol

class PlayStrategy(Protocol):
    def get_move(self, player_cards, dealer_upcard) -> str: ...