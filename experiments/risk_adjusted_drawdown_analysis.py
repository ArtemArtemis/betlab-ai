from src.models.elo import EloRating
from src.models.elo_predictor import EloPredictor
from src.models.team_form import TeamForm
from src.betting.value_detector import ValueDetector
from src.betting.risk_adjusted_stake import RiskAdjustedStake
from src.features.football_features import FootballFeatures

import pandas as pd


SEASONS = {

    "2022/23":
        "data/raw/premier_league_2022_23.csv",

    "2023/24":
        "data/raw/premier_league_2023_24.csv",

    "2024/25":
        "data/raw/premier_league_2024_25.csv"

}



class SeasonDrawdownAnalyzer:


    def __init__(self):

        self.elo = EloRating()

        self.team_form = TeamForm()

        self.predictor = EloPredictor()

        self.value_detector = ValueDetector()

        self.stake_model = RiskAdjustedStake()

        self.bankroll = 1000

        self.peak = 1000

        self.min_bankroll = 1000

        self.history = []

        self.loss_streak = 0

        self.max_loss_streak = 0

        self.bets = 0



    def run(self, df):

        df = df.sort_values(
            by="Date"
        )


        for _, match in df.iterrows():

            home = match["HomeTeam"]

            away = match["AwayTeam"]


            home_rating = self.elo.get_rating(home)

            away_rating = self.elo.get_rating(away)


            form_difference = (
                self.team_form.get_difference(
                    home,
                    away
                )
            )


            prediction = self.predictor.predict(
                home_rating,
                away_rating,
                form_difference
            )


            home_edge = (
                self.value_detector.calculate_edge(
                    prediction["home_win"],
                    match["HomeOdds"]
                )
            )


            away_edge = (
                self.value_detector.calculate_edge(
                    prediction["away_win"],
                    match["AwayOdds"]
                )
            )


            bet = None


            if self.value_detector.is_value_bet(
                home_edge["edge"]
            ):

                bet = {
                    "edge": home_edge["edge"],
                    "odds": match["HomeOdds"],
                    "win": match["FTHG"] > match["FTAG"]
                }


            elif self.value_detector.is_value_bet(
                away_edge["edge"]
            ):

                bet = {
                    "edge": away_edge["edge"],
                    "odds": match["AwayOdds"],
                    "win": match["FTAG"] > match["FTHG"]
                }



            if bet:


                self.stake_model.update_peak(
                    self.bankroll
                )


                stake = self.stake_model.get_stake(
                    bet["edge"],
                    self.bankroll
                )


                self.bets += 1


                if bet["win"]:

                    profit = (
                        stake *
                        (bet["odds"] - 1)
                    )

                    self.loss_streak = 0


                else:

                    profit = -stake

                    self.loss_streak += 1

                    self.max_loss_streak = max(
                        self.max_loss_streak,
                        self.loss_streak
                    )


                self.bankroll += profit


                self.peak = max(
                    self.peak,
                    self.bankroll
                )

                self.min_bankroll = min(
                    self.min_bankroll,
                    self.bankroll
                )


                self.history.append(
                    self.bankroll
                )



            result = (

                "H"
                if match["FTHG"] > match["FTAG"]

                else

                "A"
                if match["FTHG"] < match["FTAG"]

                else

                "D"

            )


            self.elo.update(
                home,
                away,
                result,
                match["FTHG"] - match["FTAG"]
            )


            self.team_form.update(
                home,
                away,
                result
            )



    def report(self):

        max_drawdown = 0

        peak = 1000


        for bank in self.history:

            if bank > peak:

                peak = bank


            drawdown = peak - bank


            max_drawdown = max(
                max_drawdown,
                drawdown
            )


        return {

            "bets":
                self.bets,

            "final":
                round(self.bankroll, 2),

            "profit":
                round(
                    self.bankroll - 1000,
                    2
                ),

            "max_dd":
                round(
                    max_drawdown,
                    2
                ),

            "min_bank":
                round(
                    self.min_bankroll,
                    2
                ),

            "loss_streak":
                self.max_loss_streak
        }



if __name__ == "__main__":


    print(
        "\n=============================="
    )

    print(
        "RISK ADJUSTED SEASON DRAWDOWN"
    )

    print(
        "=============================="
    )


    total_profit = 0

    total_bets = 0


    for season, path in SEASONS.items():


        df = pd.read_csv(path)

        df = FootballFeatures(df).prepare()


        analyzer = SeasonDrawdownAnalyzer()


        analyzer.run(df)


        result = analyzer.report()


        total_profit += result["profit"]

        total_bets += result["bets"]


        print(
            f"\n{season}"
        )

        print(
            f"Bets: {result['bets']}"
        )

        print(
            f"Profit: {result['profit']:+.2f}"
        )

        print(
            f"Final Bank: {result['final']:.2f}"
        )

        print(
            f"Max DD: {result['max_dd']:.2f}"
        )

        print(
            f"Min Bank: {result['min_bank']:.2f}"
        )

        print(
            f"Loss streak: {result['loss_streak']}"
        )



    print(
        "\nTOTAL"
    )

    print(
        f"Bets: {total_bets}"
    )

    print(
        f"Profit: {total_profit:+.2f}"
    )