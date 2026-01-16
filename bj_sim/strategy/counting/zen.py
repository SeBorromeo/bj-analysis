from models.card import Card

ZEN_TAGS = [
    1,  # 2
    1,  # 3
    2,  # 4
    2,  # 5
    2,  # 6
    1,  # 7
    0,  # 8
    0,  # 9
    -2,  # 10, J, Q, K
    -1   # A
]

class ZenCountingStrategy:
    def get_tag(self, card: Card) -> int:
        idx = card.value - 2
        return ZEN_TAGS[idx] if 0 <= idx < len(ZEN_TAGS) else 0