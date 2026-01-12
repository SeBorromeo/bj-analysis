from strategy.bjstrategy import BJStrategy
from models.card import Card, Rank

split_table = [
    ['SP', 'SP', 'SP', 'SP', 'SP', 'SP', 'H', 'H', 'H', 'H'], # 2-2
    ['SP', 'SP', 'SP', 'SP', 'SP', 'SP', 'H', 'H', 'H', 'H'], # 3-3
    ['H', 'H', 'H', 'SP', 'SP', 'SP', 'H', 'H', 'H', 'H'], # 4-4
    ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'H', 'H'], # 5-5
    ['SP', 'SP', 'SP', 'SP', 'SP', 'H', 'H', 'H', 'H', 'H'], # 6-6
    ['SP', 'SP', 'SP', 'SP', 'SP', 'SP', 'H', 'H', 'H', 'H'], # 7-7
    ['SP', 'SP', 'SP', 'SP', 'SP', 'SP', 'SP', 'SP', 'SP', 'SP'], # 8-8
    ['SP', 'SP', 'SP', 'SP', 'SP', 'S', 'SP', 'SP', 'S', 'S'], # 9-9
    ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'], # 10-10
    ['SP', 'SP', 'SP', 'SP', 'SP', 'S', 'SP', 'SP', 'SP', 'SP'], # 11-11
]

ace_table = [
    ['H', 'H', 'H', 'D', 'D', 'H', 'H', 'H', 'H', 'H'], # A-2
    ['H', 'H', 'H', 'D', 'D', 'H', 'H', 'H', 'H', 'H'], # A-3
    ['H', 'H', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'], # A-4
    ['H', 'H', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'], # A-5
    ['H', 'D', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'], # A-6
    ['S', 'D', 'D', 'D', 'D', 'S', 'S', 'H', 'H', 'H'], # A-7
]

total_table = [
    ['H', 'D', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'], # 9
    ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'H', 'H'], # 10
    ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'H'], # 11
    ['H', 'H', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'], # 12
    ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'], # 13
    ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'], # 14
    ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'], # 15
    ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'], # 16
]

class BJBasicStrategy(BJStrategy):
    def get_move(self, player_cards: list[Card], dealer_upcard: Card):
        if len(player_cards) < 2:
            raise ValueError("Player must have at least two cards to determine strategy.")

        total = sum(card.value for card in player_cards)

        # Handle hands with more than two cards (no splits or doubles possible)
        if len(player_cards) > 2:
            if total < 9:
                return 'H'
            elif total >= 17:
                return 'S'
            
            return total_table[total - 9][dealer_upcard.value - 2]

        # Handle two-card hands
        player_card1, player_card2 = player_cards
        if player_card1.rank == player_card2.rank:
            return split_table[player_card1.value - 2][dealer_upcard.value - 2]
        
        if player_card1.rank == Rank.ACE or player_card2.rank == Rank.ACE:
            non_ace_card = player_card1 if player_card2.rank == Rank.ACE else player_card2
            if non_ace_card.value >= 8:
                return 'S'

            return ace_table[non_ace_card.value - 2][dealer_upcard.value - 2]
        
        if total < 9:
            return 'H'
        if total >= 17:
            return 'S'
        return total_table[total - 9][dealer_upcard.value - 2]