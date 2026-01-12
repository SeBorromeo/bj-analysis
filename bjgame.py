from models.shoe import Shoe
from bjtablesettings import BJTableSettings
from models.player import Player
from stats import Stats

class BlackJackGame:
    def __init__(self, player: Player, table_settings: BJTableSettings, stats: Stats):
        self.player = player
        self.table_settings = table_settings
        self.stats = stats
        self.shoe = Shoe(self.table_settings.num_decks)
        self.current_count = 0

    def play_hand(self):
        card1, card2, card3, dealer_upcard = self.shoe.deal_card(), self.shoe.deal_card(), self.shoe.deal_card(), self.shoe.deal_card()
        player_hand = [card1, card3]
        dealer_hand = [card2, dealer_upcard]
        

        move = self.player.get_move(player_hand, dealer_upcard)



        pass
    
    def deal_card_take_count(self):
        card = self.shoe.deal_card()
        self.current_count += self.player.counting_strategy.tag(card)
        return card