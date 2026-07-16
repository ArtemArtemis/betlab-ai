from src.models.elo import EloRating
from src.models.elo_predictor import EloPredictor
from src.models.team_form import TeamForm
from src.models.historical_probability_calibrator import (
    HistoricalProbabilityCalibrator
)
from src.betting.value_detector import ValueDetector
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


WINDOWS = [
    25,
    50,
    100,
    150
]


class HistoricalCalibrationOptimizer:


    def __init__(
        self,
        window
    ):

        self.window = window

        self.elo = EloRating()

        self.team_form = TeamForm()

        self.predictor = EloPredictor()

        self.calibrator = HistoricalProbabilityCalibrator()

        self.value_detector = ValueDetector()

        self.bankroll = 1000

        self.stake = 10

        self.bets = []

        self.predictions = []

        self.results = []



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


            home_rating = self.elo.get_rating(
                home
            )

            away_rating = self.elo.get_rating(
                away
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


            if len(self.predictions) >= self.window:

                self.calibrator.fit(
                    self.predictions[-self.window:],
                    self.results[-self.window:]
                )


                home_probability = (
                    self.calibrator.calibrate(
                        prediction["home_win"]
                    )
                )

            else:

                home_probability = prediction["home_win"]



            away_probability = (
                1 - home_probability
            )



            home_edge = (
                self.value_detector.calculate_edge(
                    home_probability,
                    match["HomeOdds"]
                )
            )


            away_edge = (
                self.value_detector.calculate_edge(
                    away_probability,
                    match["AwayOdds"]
                )
            )


            if self.value_detector.is_value_bet(
                home_edge["edge"]
            ):

                win = (
                    match["FTHG"]
                    >
                    match["FTAG"]
                )


                self.record(
                    match["HomeOdds"],
                    win
                )


            elif self.value_detector.is_value_bet(
                away_edge["edge"]
            ):

                win = (
                    match["FTAG"]
                    >
                    match["FTHG"]
                )


                self.record(
                    match["AwayOdds"],
                    win
                )



            self.predictions.append(
                prediction["home_win"]
            )


            self.results.append(

                1
                if match["FTHG"] > match["FTAG"]
                else 0

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



    def record(
        self,
        odds,
        win
    ):

        if win:

            self.bankroll += (
                self.stake *
                (odds - 1)
            )

        else:

            self.bankroll -= self.stake


        self.bets.append(
            win
        )



    def report(self):

        profit = (
            self.bankroll - 1000
        )

        roi = (
            profit /
            (len(self.bets) * self.stake)
        )


        return {

            "bets":
                len(self.bets),

            "profit":
                round(
                    profit,
                    2
                ),

            "roi":
                round(
                    roi * 100,
                    2
                )

        }



if __name__ == "__main__":


    print(
        "\n=============================="
    )

    print(
        "CALIBRATION WINDOW OPTIMIZATION"
    )

    print(
        "=============================="
    )


    datasets = {}


    for season, path in SEASONS.items():

        df = pd.read_csv(path)

        datasets[season] = (
            FootballFeatures(df).prepare()
        )



    for window in WINDOWS:


        optimizer = HistoricalCalibrationOptimizer(
            window
        )


        for season, df in datasets.items():

            optimizer.run(df)


        result = optimizer.report()


        print(
            f"\nWindow: {window}"
        )

        print(
            f"Bets: {result['bets']}"
        )

        print(
            f"Profit: {result['profit']:+.2f}"
        )

        print(
            f"ROI: {result['roi']:+.2f}%"
        )