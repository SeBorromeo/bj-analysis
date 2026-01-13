class Stats:
    def __init__(self):
        self.total_hands = 0
        self.wins = 0
        self.losses = 0
        self.pushes = 0
        self.black_jacks = 0

    def record_win(self):
        self.wins += 1
        self.total_hands += 1

    def record_loss(self):
        self.losses += 1
        self.total_hands += 1

    def record_push(self):
        self.pushes += 1
        self.total_hands += 1

    def record_blackjack(self):
        self.black_jacks += 1

    def get_summary(self):
        return {
            'total_hands': self.total_hands,
            'wins': self.wins,
            'losses': self.losses,
            'pushes': self.pushes,
            'win_rate': f"{self.wins / self.total_hands:.2%}" if self.total_hands > 0 else 0,
            'loss_rate': f"{self.losses / self.total_hands:.2%}" if self.total_hands > 0 else 0,
            'push_rate': f"{self.pushes / self.total_hands:.2%}" if self.total_hands > 0 else 0,
            'blackjack_rate': f"{self.black_jacks / self.total_hands:.2%}" if self.total_hands > 0 else 0,
        }