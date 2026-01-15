from bjgame import BlackJackGame
from stats import Stats
from models.player import Player

class BJEngine:
    def __init__(self, player: Player, table_settings):
        self.player = player
        self.stats = Stats(starting_bankroll=player.bankroll)
        self.game = BlackJackGame(player, table_settings, self.stats)

    def runNSimulations(self, N_SIMULATIONS):
        for iter in range(N_SIMULATIONS):
            if iter % 1000 == 0:
                print(f"Running simulation {iter}/{N_SIMULATIONS}")
            self.game.play_round()
    
    def printResults(self):
        print("===== Simulation Results =====")
        print("Current bankroll: ", self.player.bankroll)
        print(self.stats.get_summary())