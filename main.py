from bj_sim_engine import BJEngine

def main():
    engine = BJEngine()
    while True:
        print("\n")
        input("Press Enter to run a simulation...")    
        engine.runNSimulations(1)
        engine.printResults()

    engine.runNSimulations(10000)
    engine.printResults()

if __name__ == "__main__":
    main()