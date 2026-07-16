from src.backtesting.backtester import Backtester

from src.betting.value_detector import ValueDetector

from src.models.elo import EloRating
from src.models.elo_predictor import EloPredictor
from src.models.team_form import TeamForm

from src.models.confidence_calibrator import (
    ConfidenceCalibrator
)


class ConfidenceCalibratedWalkForwardBacktester:


    def __init__(self):

        self.elo = EloRating()

        self.team_form = TeamForm()

        self.predictor = EloPredictor()

        self.confidence_calibrator = ConfidenceCalibrator(
            confidence=0.7
        )

        self.value_detector = ValueDetector()

        self.backtester = Backtester()



    def run(
        self,
        df
    ):

        print(
            "Running Confidence Calibrated Walk Forward Backtest..."
        )


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



            calibrated_home_probability = (
                self.confidence_calibrator.calibrate(
                    prediction["home_win"]
                )
            )


            calibrated_away_probability = (
                self.confidence_calibrator.calibrate(
                    prediction["away_win"]
                )
            )



            home_value = (
                self.value_detector.calculate_edge(
                    calibrated_home_probability,
                    match["HomeOdds"]
                )
            )


            away_value = (
                self.value_detector.calculate_edge(
                    calibrated_away_probability,
                    match["AwayOdds"]
                )
            )



            if self.value_detector.is_value_bet(
                home_value["edge"]
            ):


                self.backtester.place_bet(

                    probability=(
                        calibrated_home_probability
                    ),

                    odds=match["HomeOdds"],

                    result=(
                        "WIN"
                        if match["FTHG"] > match["FTAG"]
                        else "LOSS"
                    ),

                    home_team=home,

                    away_team=away,

                    date=match["Date"]
                )



            elif self.value_detector.is_value_bet(
                away_value["edge"]
            ):


                self.backtester.place_bet(

                    probability=(
                        calibrated_away_probability
                    ),

                    odds=match["AwayOdds"],

                    result=(
                        "WIN"
                        if match["FTAG"] > match["FTHG"]
                        else "LOSS"
                    ),

                    home_team=home,

                    away_team=away,

                    date=match["Date"]
                )



            # Update Elo after match

            if match["FTHG"] > match["FTAG"]:

                result = "H"


            elif match["FTHG"] < match["FTAG"]:

                result = "A"


            else:

                result = "D"



            goal_difference = (
                match["FTHG"]
                -
                match["FTAG"]
            )



            self.elo.update(
                home,
                away,
                result,
                goal_difference
            )



            self.team_form.update(
                home,
                away,
                result
            )



        self.backtester.report()


        return self.backtester.bets