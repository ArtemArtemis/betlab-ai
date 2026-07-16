from src.backtesting.backtester import Backtester

from src.betting.value_detector import ValueDetector

from src.models.elo import EloRating
from src.models.elo_predictor import EloPredictor
from src.models.team_form import TeamForm

from src.models.elo_form_blender import (
    EloFormBlender
)



class EloFormBlendWalkForwardBacktester:


    def __init__(self):

        self.elo = EloRating()

        self.team_form = TeamForm()

        self.predictor = EloPredictor()

        self.blender = EloFormBlender(
            form_weight=0.2
        )

        self.value_detector = ValueDetector()

        self.backtester = Backtester()



    def run(
        self,
        df
    ):

        print(
            "Running Elo Form Blend Walk Forward Backtest..."
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


            home_probability = (
                self.blender.blend(
                    prediction["home_win"],
                    form_difference
                )
            )


            away_probability = (
                1 - home_probability
            )



            home_value = (
                self.value_detector.calculate_edge(
                    home_probability,
                    match["HomeOdds"]
                )
            )


            away_value = (
                self.value_detector.calculate_edge(
                    away_probability,
                    match["AwayOdds"]
                )
            )



            if self.value_detector.is_value_bet(
                home_value["edge"]
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
                away_value["edge"]
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



            if match["FTHG"] > match["FTAG"]:

                result = "H"

            elif match["FTHG"] < match["FTAG"]:

                result = "A"

            else:

                result = "D"



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


        self.backtester.report()

        return self.backtester.bets