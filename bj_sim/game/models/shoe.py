from .card import Card, Rank, Suit
import random

class Shoe:
    def __init__(self, num_decks=6):
        deck = self._generate_deck()
        self.shoe = deck * num_decks
        self.discard_pile = []

        self._shuffle_shoe_and_add_shuffle_card()


    def _generate_deck(self) -> list[Card]:
        return [Card(rank, suit) for suit in Suit for rank in Rank]


    def deal_card(self) -> Card: 
        if len(self.shoe) == 0:
            # print("Shoe is empty, resetting shoe...")
            self.shoe = self.reset_shoe()

        card = self.shoe.pop(0)
        if card == 'shuffle_card':
            # print("Reshuffling the shoe...")
            self.reset_shoe()
            card = self.shoe.pop(0)
            
        self.discard_pile.append(card)
        return card
    

    def reset_shoe(self) -> None:
        self.shoe.extend(self.discard_pile)
        self.discard_pile.clear()

        self._shuffle_shoe_and_add_shuffle_card()


    def _shuffle_shoe_and_add_shuffle_card(self) -> None:
        random.shuffle(self.shoe)

        # Insert card
        self.shoe.insert(int(random.uniform(.25, .35) * len(self.shoe)), 'shuffle_card')

        # Burn first card
        self.discard_pile.append(self.shoe.pop(0))

    
    def remaining_cards(self) -> int:
        return len(self.shoe)
