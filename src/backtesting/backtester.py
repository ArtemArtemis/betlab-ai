from src.config.model_config import MODEL_CONFIG


class Backtester:

    def __init__(self):

        self.starting_bankroll = MODEL_CONFIG[
            "starting_bankroll"
        ]

        self.bankroll = self.starting_bankroll

        self.stake = MODEL_CONFIG[
            "stake"
        ]

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

        if odds is None or odds <= 1:
            return


        market_probability = (
            1 / odds
        )


        edge = (
            probability
            -
            market_probability
        )


        win = (
            result == "WIN"
        )


        if win:

            profit = (
                self.stake
                *
                (odds - 1)
            )

        else:

            profit = (
                -self.stake
            )


        self.bankroll += profit


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
                "stake": self.stake,
                "bankroll": self.bankroll
            }
        )


    def report(self):

        total_bets = len(
            self.bets
        )


        if total_bets == 0:

            print("No bets")

            return


        wins = sum(
            1
            for bet in self.bets
            if bet["win"]
        )


        losses = (
            total_bets
            -
            wins
        )


        profit = (
            self.bankroll
            -
            self.starting_bankroll
        )


        total_staked = sum(
            bet["stake"]
            for bet in self.bets
        )


        roi = (
            profit
            /
            total_staked
        )


        print(
            "\n===== BACKTEST REPORT ====="
        )

        print(
            f"Bets: {total_bets}"
        )

        print(
            f"Wins: {wins}"
        )

        print(
            f"Losses: {losses}"
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


        print(
            "\nLast 5 bets:"
        )


        for bet in self.bets[-5:]:

            print(
                bet
            )