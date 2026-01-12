from models.card import Card

class HiLo:
    def get_tag(self, card: Card) -> int:
        if card.value in {2, 3, 4, 5, 6}:
            return +1
        if card.value in {10, 11}:
            return -1
        return 0
