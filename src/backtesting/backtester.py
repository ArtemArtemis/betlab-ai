import pandas as pd


class Backtester:

    def __init__(
        self,
        starting_bankroll=1000,
        stake=10
    ):

        self.starting_bankroll = starting_bankroll
        self.bankroll = starting_bankroll
        self.stake = stake

        self.bets = []


    def place_bet(
        self,
        probability,
        odds,
        result
    ):

        market_probability = 1 / odds


        edge = (
            probability
            -
            market_probability
        )


        # Ставим только если есть преимущество
        if edge < 0.08:
            return


        win = False


        if result == "WIN":
            win = True


        if win:

            profit = (
                self.stake
                *
                (odds - 1)
            )

            self.bankroll += profit


        else:

            self.bankroll -= self.stake


        self.bets.append(
            {
                "odds": odds,
                "probability": probability,
                "edge": edge,
                "win": win,
                "bankroll": self.bankroll
            }
        )


    def report(self):

        total_bets = len(self.bets)


        if total_bets == 0:
            print("No bets")
            return


        wins = sum(
            1
            for b in self.bets
            if b["win"]
        )


        profit = (
            self.bankroll
            -
            self.starting_bankroll
        )


        roi = (
            profit
            /
            (total_bets * self.stake)
        )


        print("\n===== BACKTEST REPORT =====")

        print(
            f"Bets: {total_bets}"
        )

        print(
            f"Wins: {wins}"
        )

        print(
            f"Losses: {total_bets - wins}"
        )

        print(
            f"Bank: {self.bankroll:.2f}"
        )

        print(
            f"Profit: {profit:.2f}"
        )

        print(
            f"ROI: {roi:.2%}"
        )