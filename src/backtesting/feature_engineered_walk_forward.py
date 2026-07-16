from src.backtesting.backtester import Backtester

from src.betting.value_detector import ValueDetector

from src.models.elo import EloRating
from src.models.team_form import TeamForm

from src.models.elo_predictor_v2 import EloPredictorV2

from src.models.team_strength_features import (
    TeamStrengthFeatures
)



class FeatureEngineeredWalkForwardBacktester:


    def __init__(self):

        self.elo = EloRating()

        self.team_form = TeamForm()

        self.predictor = EloPredictorV2()

        self.features = TeamStrengthFeatures()

        self.value_detector = ValueDetector()

        self.backtester = Backtester()



    def run(
        self,
        df
    ):

        print(
            "Running Feature Engineered Walk Forward Backtest..."
        )


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


            elo_difference = (
                home_rating
                -
                away_rating
            )


            strength_feature = (
                self.features.calculate(
                    elo_difference,
                    form_difference
                )
            )


            prediction = self.predictor.predict(
                home_rating,
                away_rating,
                strength_feature
            )


            home_value = (
                self.value_detector.calculate_edge(
                    prediction["home_win"],
                    match["HomeOdds"]
                )
            )


            away_value = (
                self.value_detector.calculate_edge(
                    prediction["away_win"],
                    match["AwayOdds"]
                )
            )


            if self.value_detector.is_value_bet(
                home_value["edge"]
            ):


                self.backtester.place_bet(

                    prediction["home_win"],
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

                    prediction["away_win"],
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