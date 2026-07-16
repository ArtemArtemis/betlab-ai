from src.models.elo import EloRating
from src.models.elo_predictor import EloPredictor
from src.models.team_form import TeamForm
from src.betting.value_detector import ValueDetector
from src.betting.dynamic_stake_optimizer import DynamicStakeOptimizer
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



class DrawdownAnalyzer:


    def __init__(self):

        self.elo = EloRating()

        self.team_form = TeamForm()

        self.predictor = EloPredictor()

        self.value_detector = ValueDetector()

        self.stake_model = DynamicStakeOptimizer(
            variant="B"
        )

        self.bankroll = 1000

        self.starting_bankroll = 1000

        self.history = []

        self.loss_streak = 0

        self.max_loss_streak = 0



    def run(
        self,
        df
    ):

        df = df.sort_values(
            by="Date"
        )


        for _, match in df.iterrows():

            home = match["HomeTeam"]

            away = match["AwayTeam"]


            home_rating = (
                self.elo.get_rating(home)
            )

            away_rating = (
                self.elo.get_rating(away)
            )


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

                    "odds":
                        match["HomeOdds"],

                    "probability":
                        prediction["home_win"],

                    "edge":
                        home_edge["edge"],

                    "win":
                        match["FTHG"] > match["FTAG"]

                }


            elif self.value_detector.is_value_bet(
                away_edge["edge"]
            ):

                bet = {

                    "odds":
                        match["AwayOdds"],

                    "probability":
                        prediction["away_win"],

                    "edge":
                        away_edge["edge"],

                    "win":
                        match["FTAG"] > match["FTHG"]

                }



            if bet:


                stake = self.stake_model.edge_based(
                    bet["edge"]
                )


                if bet["win"]:

                    profit = (
                        stake *
                        (bet["odds"] - 1)
                    )

                    self.loss_streak = 0


                else:

                    profit = -stake

                    self.loss_streak += 1


                    if self.loss_streak > self.max_loss_streak:

                        self.max_loss_streak = (
                            self.loss_streak
                        )


                self.bankroll += profit


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

        peak = self.starting_bankroll

        max_drawdown = 0

        min_bankroll = self.starting_bankroll


        for bank in self.history:

            if bank > peak:

                peak = bank


            drawdown = (
                peak - bank
            )


            if drawdown > max_drawdown:

                max_drawdown = drawdown


            if bank < min_bankroll:

                min_bankroll = bank



        print(
            "\n=============================="
        )

        print(
            "DRAWDOWN ANALYSIS"
        )

        print(
            "=============================="
        )


        print(
            f"Final bankroll: {self.bankroll:.2f}"
        )

        print(
            f"Max bankroll: {max(self.history):.2f}"
        )

        print(
            f"Min bankroll: {min_bankroll:.2f}"
        )

        print(
            f"Max drawdown: {max_drawdown:.2f}"
        )

        print(
            f"Max losing streak: {self.max_loss_streak}"
        )



if __name__ == "__main__":


    analyzer = DrawdownAnalyzer()


    for season, path in SEASONS.items():

        print(
            f"\nRunning {season}"
        )


        df = pd.read_csv(path)

        df = FootballFeatures(df).prepare()

        analyzer.run(df)



    analyzer.report()