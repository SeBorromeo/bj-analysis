class Stats:
    def __init__(self, starting_bankroll: float):
        self.starting_bankroll = starting_bankroll
        self.bankroll = starting_bankroll

        self.total_hands = 0
        self.wins = 0
        self.losses = 0
        self.pushes = 0
        self.blackjacks = 0

        self.total_wagered = 0.0
        self.total_profit = 0.0 


    def record_hand(self, bet: float, payout: float, *, is_blackjack: bool = False):
        self.total_hands += 1
        self.total_wagered += bet
        self.total_profit += payout
        self.bankroll += payout

        if payout > 0:
            self.wins += 1
        elif payout < 0:
            self.losses += 1
        else:
            self.pushes += 1

        if is_blackjack:
            self.blackjacks += 1


    @property
    def ev(self) -> float:
        if self.total_wagered == 0:
            return 0.0
        return self.total_profit / self.total_wagered


    @property
    def ev_per_100(self) -> float:
        if self.total_hands == 0:
            return 0.0
        return (self.total_profit / self.total_hands) * 100


    def get_summary(self) -> dict:
        return {
            "total_hands": self.total_hands,
            "wins": self.wins,
            "losses": self.losses,
            "pushes": self.pushes,
            "win_rate": f"{self.wins / self.total_hands:.2%}",
            "loss_rate": f"{self.losses / self.total_hands:.2%}",
            "push_rate": f"{self.pushes / self.total_hands:.2%}",
            "blackjack_rate": f"{self.blackjacks / self.total_hands:.2%}",
            "total_wagered": round(self.total_wagered, 2),
            "total_profit": round(self.total_profit, 2),
            "ev": f"{self.ev:.4%}",
            "final_bankroll": round(self.bankroll, 2),
        }


    def print_summary(self):
        s = self.get_summary()
        print(f"\nCurrent bankroll: {s['final_bankroll']}")
        print({
            k: v
            for k, v in s.items()
            if k not in ("final_bankroll",)
        })
