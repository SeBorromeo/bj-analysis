class BettingRamp:
    def __init__(self, spread=None):
        if spread is None:
            self.spread = [
                (float('-inf'), 1),
                (0, 1),
                (1, 3),
                (2, 5),
                (3, 8),
                (4, 12)
            ]
        else:
            self.spread = spread


    def get_bet(self, true_count: int) -> int:
        for ramp_point in self.spread:
            if true_count <= ramp_point[0]:
                return ramp_point[1]
        return self.spread[-1][1]