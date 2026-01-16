import math
from bj_sim.game.models.shoe import Shoe
from bj_table_settings import BJTableSettings
from bj_sim.game.models.player import Player
from bj_sim.game.stats import Stats
from bj_sim.game.models.card import Card, Rank
from bj_sim.game.models.player_hand import PlayerHand

VERBOSE = False

class BlackJackGame:
    def __init__(self, player: Player, table_settings: BJTableSettings, stats: Stats):
        self.player = player
        self.table_settings = table_settings
        self.stats = stats

        self.shoe = Shoe(self.table_settings.num_decks)
        self.current_count = 0

        self.verbose = VERBOSE


    def play_round(self) -> None:
        # If can add more hands in middle of shoe:
        num_hands = 1 # TODO: Use player decision based on count and deviation strategy

        if num_hands <= 0:
            raise ValueError("Number of hands must be at least 1.")

        TC = self._get_current_true_count()
        bet_mult = self.player.bet_spread.get_bet(TC)
        bet = 10 * bet_mult

        # Deal initial cards
        players_hands_cards, dealer_cards = self._initial_deal(num_hands)
        dealer_upcard = dealer_cards[1]

        hands = [PlayerHand(cards, bet) for cards in players_hands_cards]

        if self._check_blackjack(dealer_cards):
            if self.verbose:
                print(f"Dealer has blackjack with hand {dealer_cards}")
            
            self._evaluate_hands(hands, dealer_total=21)
            return
        
        num_splits = 0
        for i, curr_hand in enumerate(hands):
            if self.verbose:
                print(f"Hand is {curr_hand}, Dealer upcard is {dealer_upcard}")

            if self._check_blackjack(curr_hand.cards):
                continue

            hand_over = False
            while not hand_over:
                # Ensure hand has at least two cards (single cards can be left over from splits)
                if len(curr_hand.cards) == 1:
                    new_card = self._deal_card_take_count()
                    curr_hand.add_card(new_card)

                    if self.verbose:
                        print(f"Dealing second card: {new_card}")

                TC = self._get_current_true_count()

                move = self.player.get_move(curr_hand, dealer_upcard, TC)

                if move not in ['H', 'S', 'D', 'DS', 'SP', 'SPD', 'RH']:
                    raise ValueError(f"Invalid move: {move}")

                if move == 'RH' and self.table_settings.allow_surrender:
                    if self.verbose:
                        print("Surrendering hand")

                    curr_hand.surrender = True

                    hand_over = True
                elif move == 'SP' or (move == 'SPD' and self.table_settings.double_after_split):
                    num_splits += 1
                    if num_splits > self.table_settings.max_splits:
                        if self.verbose:
                            print("Max splits reached, cannot split further.")

                        hand_over = True
                        continue

                    if self.verbose:
                        print("Splitting hand")

                    second_card = curr_hand.cards.pop()
                    hands.insert(i + 1, PlayerHand([second_card], curr_hand.bet))
                elif (move == 'D' or move == 'DS') and (self.table_settings.double_after_split or not self.table_settings.double_after_split and num_splits == 0):
                    hand_over = True
                    self._double(curr_hand)
                elif move == 'S' or move == 'DS':
                    if self.verbose:
                        print("Standing")
                    
                    hand_over = True
                else:
                    hand_over = self._hit(curr_hand)
                    
        if self.verbose:
            print(f"Dealer hand is {dealer_cards}")

        # Dealer plays hand
        dealer_total = self._play_dealer_hand(dealer_cards)
        
        if self.verbose:
            print(f"Dealer final hand: {dealer_cards}")

        self._evaluate_hands(hands, dealer_total)


    def _split(self, hands: list[PlayerHand], curr_hand: PlayerHand) -> PlayerHand:
        pass


    def _double(self, hand: PlayerHand) -> None:
        hand.bet *= 2
        new_card = self._deal_card_take_count()
        hand.add_card(new_card)

        if self.verbose:
            print("Doubling down, new card: ", new_card)


    def _hit(self, hand: PlayerHand) -> bool:
        new_card = self._deal_card_take_count()

        if self.verbose:
            print(f"Drew card: {new_card}")

        hand.add_card(new_card)

        if hand.value > 21: # Bust
            if self.verbose:
                print("Busted!")
            return True
        return False


    def _initial_deal(self, num_hands: int) -> tuple[list[list[Card]], list[Card]]:
        players_hands_cards = [[] for _ in range(num_hands)]
        dealer_cards = []
        
        for _ in range(2):
            for i in range(num_hands):
                players_hands_cards[i].append(self._deal_card_take_count())
            dealer_cards.append(self._deal_card_take_count())
                
        return players_hands_cards, dealer_cards

    
    def _deal_card_take_count(self) -> Card:
        card = self.shoe.deal_card()
        self.current_count += self.player.counting_strategy.get_tag(card)
        return card
    

    def _play_dealer_hand(self, dealer_hand: list[Card]) -> int:
        dealer_total = sum(card.value for card in dealer_hand)
        dealer_soft = any(card.rank == Rank.ACE for card in dealer_hand)

        while dealer_total < 17 or (dealer_total == 17 and dealer_soft and self.table_settings.dealer_hits_soft_17):
            new_card = self._deal_card_take_count()
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
    

    def _evaluate_hands(self, player_hands: list[PlayerHand], dealer_total: int) -> None:
        for hand in player_hands:
            if hand.surrender:
                self.player.bankroll -= hand.bet / 2
                self.stats.record_hand(bet=hand.bet, payout=hand.bet / 2, is_blackjack=False)
            elif self._check_blackjack(hand.cards):
                if dealer_total == 21:
                    self.stats.record_hand(bet=hand.bet, payout=0, is_blackjack=False)
                else:
                    self.player.bankroll += self.table_settings.payout_blackjack * hand.bet
                    self.stats.record_hand(bet=hand.bet, payout=self.table_settings.payout_blackjack * hand.bet, is_blackjack=True)
            elif hand.value > 21 or hand.value < dealer_total <= 21: 
                self.player.bankroll -= hand.bet
                self.stats.record_hand(bet=hand.bet, payout=-hand.bet, is_blackjack=False)
            elif dealer_total > 21 or hand.value > dealer_total:
                self.player.bankroll += self.table_settings.payout * hand.bet
                self.stats.record_hand(bet=hand.bet, payout=self.table_settings.payout * hand.bet, is_blackjack=False)
            else:
                self.stats.record_hand(bet=hand.bet, payout=0, is_blackjack=False)

                
    def _check_blackjack(self, cards: list[Card]) -> bool:
        return len(cards) == 2 and sum(card.value for card in cards) == 21
    

    def _get_current_true_count(self) -> int:
        remaining_decks = self.shoe.remaining_cards() / 52
        rounded_remaining_decks = math.ceil(remaining_decks * 2) / 2 # rounds up to nearest 0.5
        if rounded_remaining_decks == 0:
            return 0
        return self.current_count // rounded_remaining_decks