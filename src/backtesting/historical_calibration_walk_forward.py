from src.backtesting.backtester import Backtester

from src.betting.value_detector import ValueDetector

from src.models.elo import EloRating
from src.models.elo_predictor import EloPredictor
from src.models.team_form import TeamForm

from src.models.historical_probability_calibrator import (
    HistoricalProbabilityCalibrator
)



class HistoricalCalibrationWalkForwardBacktester:


    def __init__(self):

        self.elo = EloRating()

        self.team_form = TeamForm()

        self.predictor = EloPredictor()

        self.calibrator = (
            HistoricalProbabilityCalibrator()
        )

        self.value_detector = ValueDetector()

        self.backtester = Backtester()


        self.history_predictions = []

        self.history_results = []



    def run(
        self,
        df
    ):


        print(
            "Running Historical Calibration Walk Forward..."
        )


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


            prediction = (
                self.predictor.predict(
                    home_rating,
                    away_rating,
                    form_difference
                )
            )



            if len(
                self.history_predictions
            ) > 50:


                self.calibrator.fit(
                    self.history_predictions,
                    self.history_results
                )


                home_probability = (
                    self.calibrator.calibrate(
                        prediction["home_win"]
                    )
                )

                away_probability = (
                    1 -
                    home_probability
                )


            else:

                home_probability = (
                    prediction["home_win"]
                )

                away_probability = (
                    prediction["away_win"]
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


                self.backtester.place_bet(

                    home_probability,

                    match["HomeOdds"],

                    "WIN"
                    if match["FTHG"] > match["FTAG"]
                    else "LOSS",

                    home,

                    away,

                    match["Date"]

                )



            elif self.value_detector.is_value_bet(
                away_edge["edge"]
            ):


                self.backtester.place_bet(

                    away_probability,

                    match["AwayOdds"],

                    "WIN"
                    if match["FTAG"] > match["FTHG"]
                    else "LOSS",

                    home,

                    away,

                    match["Date"]

                )



            result = (

                1
                if match["FTHG"] > match["FTAG"]
                else 0

            )


            self.history_predictions.append(
                prediction["home_win"]
            )

            self.history_results.append(
                result
            )



            elo_result = (

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
                elo_result,
                match["FTHG"] - match["FTAG"]
            )


            self.team_form.update(
                home,
                away,
                elo_result
            )



        self.backtester.report()


        return self.backtester.bets