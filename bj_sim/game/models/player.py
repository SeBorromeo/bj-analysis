from .card import Card
from bj_sim.strategy.betting.betting_ramp import BettingRamp
from bj_sim.strategy.betting.bettingstrategy import BettingStrategy

from bj_sim.strategy.counting.countingstrategy import CountingStrategy
from bj_sim.strategy.counting.hilo import HiLoCountingStrategy
from bj_sim.strategy.play.playstrategy import PlayStrategy
from bj_sim.strategy.play.basic import BasicPlayStrategy

class Player:
    def __init__(self, 
        name: str, 
        bankroll: int, 
        bj_strategy: PlayStrategy = BasicPlayStrategy(), 
        betting_strategy: BettingStrategy = BettingRamp(), 
        counting_strategy: CountingStrategy = HiLoCountingStrategy(),
        deviation_strategy={}
    ):
        self.name = name
        self.bankroll = bankroll
        self.bj_strategy = bj_strategy
        self.betting_strategy = betting_strategy
        self.counting_strategy = counting_strategy
        self.deviation_strategy = deviation_strategy
    
    def get_move(self, player_cards: list[Card], dealer_upcard: Card, true_count: int) -> str:
        return self.bj_strategy.get_move(player_cards, dealer_upcard)