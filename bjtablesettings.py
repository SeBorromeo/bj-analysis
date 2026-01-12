class BJTableSettings:
    def __init__(self, num_decks=6, dealer_hits_soft_17=False, double_after_split=True, allow_surrender=False,
        payout_blackjack=1.5, insurance_payout=2, side_bets=None, penetration=0.75, shuffle_point=None, cut_card_position=None,
        resplit_aces=False, max_splits=3, min_bet=5, max_bet=500, table_limits=None, continuous_shuffle_machine=False, 
        num_hands=1, payout=1.5
    ):
        self.num_decks = num_decks
        self.dealer_hits_soft_17 = dealer_hits_soft_17
        self.double_after_split = double_after_split
        self.allow_surrender = allow_surrender
        self.payout = payout