from bjgame import BlackJackGame
from stats import Stats

class BJEngine:
    def __init__(self, player, table_settings):
        self.stats = Stats()
        self.game = BlackJackGame(player, table_settings, self.stats)

    def runNSimulations(self, N_SIMULATIONS):
        for _ in range(N_SIMULATIONS):
            self.game.player_hand()
    
    def printResults(self):
        print(self.stats.get_summary())