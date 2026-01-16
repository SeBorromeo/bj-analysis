from typing import Protocol

class BettingStrategy(Protocol):
    def get_bet(self, true_count: int, bankroll: int) -> int: ...