from models.shoe import Shoe
from bjtablesettings import BJTableSettings
from models.player import Player
from stats import Stats
from typing import List, Tuple
from models.card import Card, Rank
from models.playerHand import PlayerHand

VERBOSE = True

class BlackJackGame:
    def __init__(self, player: Player, table_settings: BJTableSettings, stats: Stats):
        self.player = player
        self.table_settings = table_settings
        self.stats = stats

        self.shoe = Shoe(self.table_settings.num_decks)
        self.current_count = 0

        self.verbose = VERBOSE

    def play_hand(self) -> None:
        TC = self.current_count / (self.shoe.remaining_cards() / 52)

        # If can add more hands in middle of shoe:
        num_hands = 1 # TODO: Use player decision based on count and deviation strategy

        bet = 10 # TODO: Use bet spread and count to determine bet size

        # Deal initial cards
        players_hands_cards, dealer_hand = self.initial_deal(num_hands)
        dealer_upcard = dealer_hand[1]

        hands = [PlayerHand(cards, bet) for cards in players_hands_cards]

        for i, curr_hand in enumerate(hands):
            if self.verbose:
                print(f"Hand is {curr_hand}, Dealer upcard is {dealer_upcard}")

            hand_over = False
            while not hand_over:
                # Ensure hand has at least two cards (single cards can be left over from splits)
                if len(curr_hand.cards) == 1:
                    new_card = self.deal_card_take_count()
                    curr_hand.add_card(new_card)

                    if self.verbose:
                        print(f"Dealing second card: {new_card}")

                move = self.player.get_move(curr_hand.cards, dealer_upcard)

                if move not in ['H', 'S', 'D', 'SP']:
                    raise ValueError(f"Invalid move: {move}")

                if move == 'SP': # Handle split logic'
                    if self.verbose:
                        print("Splitting hand")

                    second_card = curr_hand.cards.pop()
                    hands.insert(i + 1, PlayerHand([second_card], curr_hand.bet))
                elif move == 'D': # Handle double logic
                    hand_over = True
                    curr_hand.bet *= 2
                    last_card = self.deal_card_take_count()
                    curr_hand.add_card(last_card)

                    if self.verbose:
                        print("Doubling down, new card: ", last_card)
                elif move == 'S': # Handle stand logic
                    if self.verbose:
                        print("Standing")
                    
                    hand_over = True
                else: # Handle hit logic
                    new_card = self.deal_card_take_count()

                    if self.verbose:
                        print(f"Drew card: {new_card}")

                    curr_hand.add_card(new_card)

                    if curr_hand.value > 21: # Bust
                        if self.verbose:
                            print("Busted!")
                        hand_over = True
                    
        if self.verbose:
            print(f"Dealer hand is {dealer_hand}")

        # Dealer plays hand
        dealer_total = self.play_dealer_hand(dealer_hand)
        
        if self.verbose:
            print(f"Dealer final hand: {dealer_hand}")

        self.evaluate_hands(hands, dealer_total)


    def initial_deal(self, num_hands: int) -> Tuple[List[List[Card]], List[Card]]:
        players_hands_cards = [[] for _ in range(num_hands)]
        dealer_cards = []
        
        for _ in range(2):
            for i in range(num_hands):
                players_hands_cards[i].append(self.shoe.deal_card())
            dealer_cards.append(self.shoe.deal_card())
                
        return players_hands_cards, dealer_cards

    
    def deal_card_take_count(self) -> Card:
        card = self.shoe.deal_card()
        self.current_count += self.player.counting_strategy.get_tag(card)
        return card
    
    def play_dealer_hand(self, dealer_hand: List[Card]) -> int:
        dealer_total = sum(card.value for card in dealer_hand)
        dealer_soft = any(card.rank == Rank.ACE for card in dealer_hand)

        while dealer_total < 17 or (dealer_total == 17 and dealer_soft and self.table_settings.dealer_hits_soft_17):
            new_card = self.deal_card_take_count()
            dealer_hand.append(new_card)

            if new_card.rank == Rank.ACE:
                if dealer_total + 11 <= 21:
                    dealer_total += 11
                    dealer_soft = True
                else:
                    dealer_total += 1
            else:
                dealer_total += new_card.value
                if dealer_total > 21 and dealer_soft:
                    dealer_total -= 10
                    dealer_soft = False
        
        return dealer_total
    

    def evaluate_hands(self, player_hands: list[PlayerHand], dealer_total: int) -> None:
        for hand in player_hands:
            if hand.value > 21:
                self.player.bankroll -= hand.bet
                self.stats.record_loss()
            elif dealer_total > 21 or hand.value > dealer_total:
                self.player.bankroll += self.table_settings.payout * hand.bet
                self.stats.record_win()
            elif hand.value < dealer_total:
                self.player.bankroll -= hand.bet
                self.stats.record_loss()
            else:
                self.stats.record_push()