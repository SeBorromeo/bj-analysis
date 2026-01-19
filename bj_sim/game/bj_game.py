import math
from .bj_table_settings import BJTableSettings
from bj_sim.game.models.shoe import Shoe
from bj_sim.strategy.play.playstrategy import PlayMove
from bj_sim.game.player import Player
from bj_sim.observers.stats import Stats
from bj_sim.game.models.card import Card
from bj_sim.game.models.hand import Hand
from bj_sim.game.models.player_hand import PlayerHand

HIT, STAND, DOUBLE, DOUBLE_STAND, SPLIT, SPLIT_IF_DAS, SURRENDER_HIT = (
    PlayMove.HIT,
    PlayMove.STAND,
    PlayMove.DOUBLE,
    PlayMove.DOUBLE_STAND,
    PlayMove.SPLIT,
    PlayMove.SPLIT_IF_DAS,
    PlayMove.SURRENDER_HIT,
)

class BlackJackGame:
    def __init__(self, player: Player, table_settings: BJTableSettings, stats: Stats, log_enabled: bool = False):
        self.player = player
        self.table_settings = table_settings
        self.stats = stats
        self.log_enabled = log_enabled

        self.shoe = Shoe(self.table_settings.num_decks)
        self._current_count = 0


    def play_round(self) -> None:
        true_count = self._get_current_true_count()

        # If can add more hands in middle of shoe:
        num_hands = 1 # TODO: Use player decision based on count and deviation strategy

        if num_hands <= 0:
            raise ValueError("Number of hands must be at least 1")

        bet_mult = self.player.betting_strategy.get_bet(true_count)
        bet = 10 * bet_mult

        self._log(f"Starting new round. True count: {true_count}, betting {bet} on {num_hands} hand(s)")

        # Deal initial cards
        player_hands, dealer_hand = self._initial_deal(bet, num_hands)
        dealer_upcard = dealer_hand.cards[0]

        if self._check_blackjack(dealer_hand):
            self._log(f"Dealer has blackjack with hand {dealer_hand}")
        else:
            self._play_player_hands(player_hands, dealer_upcard)
            self._play_dealer_hand(dealer_hand)

        self._evaluate_hands(player_hands, dealer_hand)


    def _double(self, hand: PlayerHand) -> None:
        hand.double_bet()
        new_card = self._deal_card_take_count()
        hand.add_card(new_card)

        self._log(f"Doubling down, new card: {new_card}")


    def _hit(self, hand: PlayerHand) -> bool:
        new_card = self._deal_card_take_count()

        self._log(f"Drew card: {new_card}")

        hand.add_card(new_card)

        if hand.value > 21: # Bust
            self._log("Busted!")
            return True
        return False


    def _initial_deal(self, bet: int, num_hands: int) -> tuple[list[PlayerHand], Hand]:
        players_hands, dealer_hand = [PlayerHand([], bet) for _ in range(num_hands)], Hand()
        
        for _ in range(2): # Two rounds of dealing
            for i in range(num_hands):
                players_hands[i].add_card(self._deal_card_take_count())
            dealer_hand.add_card(self._deal_card_take_count())
                
        return players_hands, dealer_hand

    
    def _deal_card_take_count(self) -> Card:
        card = self.shoe.deal_card()
        self._current_count += self.player.counting_strategy.get_tag(card)
        return card
    

    def _play_player_hands(self, hands: list[PlayerHand], dealer_upcard: Card) -> None:
        num_splits = 0
        for i, curr_hand in enumerate(hands):
            self._log(f"Hand is {curr_hand}, Dealer upcard is {dealer_upcard}")

            if self._check_blackjack(curr_hand):
                continue

            hand_over = False
            while not hand_over:
                # Ensure hand has at least two cards (single cards can be left over from splits)
                if len(curr_hand.cards) == 1:
                    self._hit(curr_hand)

                true_count = self._get_current_true_count()
                move = self.player.get_move(curr_hand, dealer_upcard, true_count)

                if not isinstance(move, PlayMove):
                    raise ValueError(f"Invalid move: {move}")

                if move == SURRENDER_HIT and self.table_settings.allow_surrender:
                    self._log("Surrendering hand")
                    curr_hand.surrender_hand()
                    hand_over = True
                elif (move == SPLIT or (move == SPLIT_IF_DAS and self.table_settings.double_after_split)) and num_splits < self.table_settings.max_splits:
                    num_splits += 1
                    if num_splits == self.table_settings.max_splits:
                        self._log("Max splits reached, cannot split further.")

                    self._log("Splitting hand")

                    second_card = curr_hand.split_cards()
                    hands.insert(i + 1, PlayerHand([second_card], curr_hand.bet))
                elif (move == DOUBLE or move == DOUBLE_STAND) and (self.table_settings.double_after_split or num_splits == 0):
                    self._double(curr_hand)
                    hand_over = True
                elif move == STAND or move == DOUBLE_STAND:
                    self._log("Standing")
                    hand_over = True
                else:
                    hand_over = self._hit(curr_hand)


    def _play_dealer_hand(self, dealer_hand: Hand) -> int:
        self._log(f"Dealer hand is {dealer_hand}")

        while dealer_hand.value < 17 or (dealer_hand.value == 17 and dealer_hand.is_soft and self.table_settings.dealer_hits_soft_17):
            dealer_hand.add_card(self._deal_card_take_count())

        self._log(f"Dealer final hand: {dealer_hand}")
    

    def _evaluate_hands(self, player_hands: list[PlayerHand], dealer_hand: Hand) -> None:
        for hand in player_hands:
            payout = 0
            if hand.surrender:
                payout = -hand.bet / 2
            elif self._check_blackjack(hand) and not self._check_blackjack(dealer_hand):
                payout = self.table_settings.payout_blackjack * hand.bet
            elif hand.value > 21 or hand.value < dealer_hand.value <= 21: 
                payout = -hand.bet
            elif dealer_hand.value > 21 or hand.value > dealer_hand.value:
                payout = self.table_settings.payout * hand.bet
            
            self.player.bankroll += payout
            self.stats.record_hand(bet=hand.bet, payout=payout, is_blackjack=self._check_blackjack(hand))
            

                
    def _check_blackjack(self, hand: Hand) -> bool:
        return len(hand.cards) == 2 and hand.value == 21


    def _get_current_true_count(self) -> int:
        remaining_decks = self.shoe.remaining_cards() / 52
        rounded_remaining_decks = math.ceil(remaining_decks * 2) / 2 # rounds up to nearest 0.5
        if rounded_remaining_decks == 0:
            return 0
        return int(self._current_count / rounded_remaining_decks)
    

    def _log(self, message: str) -> None:
        if self.log_enabled:
            print(message)

