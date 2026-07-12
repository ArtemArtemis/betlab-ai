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
        result,
        home_team=None,
        away_team=None,
        date=None
    ):

        market_probability = 1 / odds


        edge = (
            probability
            -
            market_probability
        )


        if edge < 0.05:
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

            profit = -self.stake

            self.bankroll -= self.stake



        self.bets.append(
            {
                "date": date,
                "home_team": home_team,
                "away_team": away_team,
                "odds": odds,
                "probability": probability,
                "market_probability": market_probability,
                "edge": edge,
                "win": win,
                "profit": profit,
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
            for bet in self.bets
            if bet["win"]
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


        print("\nLast 5 bets:")

        for bet in self.bets[-5:]:

            print(bet)