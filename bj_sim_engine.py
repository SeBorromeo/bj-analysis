from bj_sim import Player, Stats, BlackJackGame, BJTableSettings, BettingRamp, ZenCountingStrategy

class BJEngine:
    def __init__(self, verbose: bool = False):
        self.player = Player(name="TestPlayer", 
            bankroll=1000,
            betting_strategy = BettingRamp([
                (float('-inf'), 1),
                (0, 1),
                (1, 1),
                (2, 2),
                (3, 4),
                (4, 6),
                (5, 8)
            ]),      
            counting_strategy=ZenCountingStrategy()
        )
        self.table_settings = BJTableSettings() # default settings
        self.stats = Stats(starting_bankroll=self.player.bankroll)
        self.game = BlackJackGame(self.player, self.table_settings, self.stats, log_enabled=verbose)


    def runNSimulations(self, N_SIMULATIONS):
        for iter in range(N_SIMULATIONS):
            if N_SIMULATIONS >= 10000 and iter % 1000 == 0:
                print(f"Running simulation {iter}/{N_SIMULATIONS}")
            self.game.play_round()


    def printResults(self):
        print("===== Simulation Results =====")
        print("Current bankroll: ", self.player.bankroll)
        print(self.stats.get_summary())

