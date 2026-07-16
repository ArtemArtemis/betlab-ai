from src.models.elo import EloRating
from src.models.dynamic_three_way_probability import (
    DynamicThreeWayProbability
)

from src.betting.value_detector import ValueDetector
from src.backtesting.backtester import Backtester



class DynamicThreeWayWalkForwardBacktester:


    def __init__(self):

        self.elo = EloRating()

        self.predictor = DynamicThreeWayProbability()

        self.value_detector = ValueDetector()

        self.backtester = Backtester()



    def run(self, df):

        print(
            "Running Dynamic Three Way Walk Forward Backtest..."
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


            prediction = (
                self.predictor.predict(
                    home_rating,
                    away_rating
                )
            )


            outcomes = [

                {
                    "side": "H",
                    "probability":
                        prediction["home_win"],
                    "odds":
                        match["HomeOdds"]
                },

                {
                    "side": "D",
                    "probability":
                        prediction["draw"],
                    "odds":
                        match["DrawOdds"]
                },

                {
                    "side": "A",
                    "probability":
                        prediction["away_win"],
                    "odds":
                        match["AwayOdds"]
                }

            ]


            best_bet = None
            best_edge = 0


            for outcome in outcomes:

                edge = (
                    self.value_detector.calculate_edge(
                        outcome["probability"],
                        outcome["odds"]
                    )
                )


                if edge["edge"] > best_edge:

                    best_edge = edge["edge"]
                    best_bet = outcome



            if (
                best_bet
                and
                self.value_detector.is_value_bet(
                    best_edge
                )
            ):


                if match["FTHG"] > match["FTAG"]:

                    result = "H"

                elif match["FTHG"] < match["FTAG"]:

                    result = "A"

                else:

                    result = "D"


                bet_result = (
                    "WIN"
                    if result == best_bet["side"]
                    else "LOSS"
                )


                self.backtester.place_bet(
                    best_bet["probability"],
                    best_bet["odds"],
                    bet_result,
                    home,
                    away,
                    match["Date"]
                )


            # Elo update

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


        self.backtester.report()

        return self.backtester.bets