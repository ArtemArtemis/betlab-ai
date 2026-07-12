from src.models.elo import EloRating
from src.models.three_way_probability import ThreeWayProbability

from src.betting.value_detector import ValueDetector
from src.backtesting.backtester import Backtester



class ThreeWayProbabilityWalkForwardBacktester:


    def __init__(self):

        self.elo = EloRating()

        self.predictor = ThreeWayProbability()

        self.value_detector = ValueDetector()

        self.backtester = Backtester()



    def run(self, df):

        print(
            "Running Three Way Probability Walk Forward Backtest..."
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


                if (
                    edge["edge"]
                    >
                    best_edge
                ):

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



                bet_win = (
                    result == best_bet["side"]
                )


                bet_result = (
                    "WIN"
                    if bet_win
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



            # update elo

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