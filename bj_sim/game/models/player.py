from bj_sim.strategy.betting.betting_ramp import BettingRamp
from bj_sim.strategy.betting.bettingstrategy import BettingStrategy
from models.card import Card
from strategy.bjstrategy import BJStrategy
from strategy.hilocounting import HiLo
from strategy.countingstrategy import CountingStrategy
from strategy.bjbasicstrategy import BJBasicStrategy

class Player:
    def __init__(self, 
        name: str, 
        bankroll: int, 
        bj_strategy: BJStrategy = BJBasicStrategy(), 
        bet_spread: BettingStrategy = BettingRamp(), 
        counting_strategy: CountingStrategy = HiLo(),
        deviation_strategy={}
    ):
        self.name = name
        self.bankroll = bankroll
        self.bj_strategy = bj_strategy
        self.bet_spread = bet_spread
        self.counting_strategy = counting_strategy
        self.deviation_strategy = deviation_strategy
    
    def get_move(self, player_cards: list[Card], dealer_upcard: Card, true_count: int) -> str:
        return self.bj_strategy.get_move(player_cards, dealer_upcard)