from abc import ABC, abstractmethod

class BJStrategy:
    @abstractmethod
    def get_move(self, player_cards, dealer_upcard):
        pass