from bjengine import BJEngine
from models.player import Player
from bjtablesettings import BJTableSettings

def main():
    player = Player(name="TestPlayer", bankroll=1000)
    table_settings = BJTableSettings() # default settings

    engine = BJEngine(player, table_settings)
    engine.runNSimulations(1000)
    engine.printResults()

if __name__ == "__main__":
    main()