from bjgame import BlackJackGame
from stats import Stats

class BJEngine:
    def __init__(self, player, table_settings):
        self.stats = Stats()
        self.player = player
        self.game = BlackJackGame(player, table_settings, self.stats)

    def runNSimulations(self, N_SIMULATIONS):
        for _ in range(N_SIMULATIONS):
            self.game.play_hand()
    
    def printResults(self):
        print("===== Simulation Results =====")
        print("Current bankroll: ", self.player.bankroll)
        print(self.stats.get_summary())