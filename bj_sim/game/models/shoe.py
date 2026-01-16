from .card import Card, Rank, Suit
import random

class Shoe:
    def __init__(self, num_decks=6):
        self.num_decks = num_decks
        self.shoe = self.create_shoe()

    def generate_deck(self) -> list[Card]:
        return [Card(rank, suit) for suit in Suit for rank in Rank]

    def create_shoe(self) -> list[Card | str]:
        deck = self.generate_deck()
        shoe = deck * self.num_decks

        random.shuffle(shoe)

        # Insert card
        shoe.insert(int(random.uniform(.25, .35) * len(shoe)), 'shuffle_card')

        # Burn first card
        shoe.pop(0)

        return shoe

    def deal_card(self) -> Card: 
        if len(self.shoe) == 0:
            # print("Shoe is empty, creating a new shoe...")
            self.shoe = self.create_shoe()

        card = self.shoe.pop(0)
        if card == 'shuffle_card':
            # print("Reshuffling the shoe...")
            self.shoe = self.create_shoe()
            card = self.shoe.pop(0)
        
        return card
    
    def remaining_cards(self) -> int:
        return len(self.shoe)
