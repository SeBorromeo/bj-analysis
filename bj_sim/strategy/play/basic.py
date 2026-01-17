from bj_sim.game.models.card import Card
from bj_sim.game.models.player_hand import PlayerHand
from .playstrategy import PlayMove

split_table = [
    ['SPD', 'SPD', 'SP', 'SP', 'SP', 'SP', 'H', 'H', 'H', 'H'], # 2-2
    ['SPD', 'SPD', 'SP', 'SP', 'SP', 'SP', 'H', 'H', 'H', 'H'], # 3-3
    ['H', 'H', 'H', 'SPD', 'SPD', 'SPD', 'H', 'H', 'H', 'H'], # 4-4
    ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'H', 'H'], # 5-5
    ['SPD', 'SP', 'SP', 'SP', 'SP', 'H', 'H', 'H', 'H', 'H'], # 6-6
    ['SP', 'SP', 'SP', 'SP', 'SP', 'SP', 'H', 'H', 'H', 'H'], # 7-7
    ['SP', 'SP', 'SP', 'SP', 'SP', 'SP', 'SP', 'SP', 'SP', 'SP'], # 8-8
    ['SP', 'SP', 'SP', 'SP', 'SP', 'S', 'SP', 'SP', 'S', 'S'], # 9-9
    ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'], # 10-10
    ['SP', 'SP', 'SP', 'SP', 'SP', 'SP', 'SP', 'SP', 'SP', 'SP'], # A-A
]

ace_table = [
    ['H', 'H', 'H', 'D', 'D', 'H', 'H', 'H', 'H', 'H'], # A-2 (soft 13)
    ['H', 'H', 'H', 'D', 'D', 'H', 'H', 'H', 'H', 'H'], # A-3 (soft 14)
    ['H', 'H', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'], # A-4 (soft 15)
    ['H', 'H', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'], # A-5 (soft 16)
    ['H', 'D', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'], # A-6 (soft 17)
    ['S', 'DS', 'DS', 'DS', 'DS', 'S', 'S', 'H', 'H', 'H'], # A-7 (soft 18)
]

total_table = [
    ['H', 'D', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'], # 9
    ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'H', 'H'], # 10
    ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'H'], # 11
    ['H', 'H', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'], # 12
    ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'], # 13
    ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'], # 14
    ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'RH', 'H'], # 15
    ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'RH', 'RH', 'RH'], # 16
]

class BasicPlayStrategy:
    def get_move(self, hand: PlayerHand, dealer_upcard: Card) -> PlayMove:
        if len(hand.cards) < 2:
            raise ValueError("Player must have at least two cards to determine strategy.")

        # Handle split
        if len(hand.cards) == 2 and hand.cards[0].rank == hand.cards[1].rank:
            return PlayMove(split_table[hand.cards[0].value - 2][dealer_upcard.value - 2])

        # Handle soft totals
        if hand.is_soft:
            total_without_ace = hand.value - 11
            if total_without_ace >= 8:
                return PlayMove.STAND
            return PlayMove(ace_table[total_without_ace - 2][dealer_upcard.value - 2])

        # Handle hard totals        
        return self._get_move_from_total(hand.value, dealer_upcard)

    def _get_move_from_total(self, total: int, dealer_upcard: Card) -> PlayMove:
        if total < 9:
            return PlayMove.HIT
        if total >= 17:
            return PlayMove.STAND
        return PlayMove(total_table[total - 9][dealer_upcard.value - 2])