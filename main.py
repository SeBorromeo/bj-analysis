from bjengine import BJEngine
from models.betspread import BetSpread
from models.player import Player
from bjtablesettings import BJTableSettings

def main():
    player = Player(name="TestPlayer", bankroll=1000,
        bet_spread = BetSpread([
            (float('-inf'), 1),
            (0, 1),
            (1, 3),
            (2, 5),
            (3, 8),
            (4, 12)
        ]),              
    )
    table_settings = BJTableSettings() # default settings

    engine = BJEngine(player, table_settings)
    while True:
        print("\n")
        input("Press Enter to run a simulation...")    
        engine.runNSimulations(1)
        engine.printResults()

    engine.runNSimulations(100000)
    engine.printResults()

if __name__ == "__main__":
    main()