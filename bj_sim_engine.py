from bj_sim import Player, Stats, BlackJackGame, BJTableSettings, BettingRamp, ZenCountingStrategy

class BJEngine:
    def __init__(self):
        self.player = Player(name="TestPlayer", bankroll=1000,
            betting_strategy = BettingRamp([
                (float('-inf'), 1),
                (0, 1),
                (1, 3),
                (2, 5),
                (3, 8),
                (4, 12)
            ]),              
        )
        self.table_settings = BJTableSettings() # default settings
        self.stats = Stats(starting_bankroll=self.player.bankroll)
        self.game = BlackJackGame(self.player, self.table_settings, self.stats)

    def runNSimulations(self, N_SIMULATIONS):
        for iter in range(N_SIMULATIONS):
            if iter % 1000 == 0:
                print(f"Running simulation {iter}/{N_SIMULATIONS}")
            self.game.play_round()
    
    def printResults(self):
        print("===== Simulation Results =====")
        print("Current bankroll: ", self.player.bankroll)
        print(self.stats.get_summary())