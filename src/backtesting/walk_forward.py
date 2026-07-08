from src.models.elo import EloRating
from src.models.elo_predictor import EloPredictor
from src.backtesting.backtester import Backtester


class WalkForwardBacktester:

    def __init__(self):

        self.elo = EloRating()

        self.predictor = EloPredictor()

        self.backtester = Backtester()


    def run(self, df):

        print("Running Walk Forward Backtest...")


        df = df.sort_values(
            by="Date"
        )


        for _, match in df.iterrows():

            home = match["HomeTeam"]

            away = match["AwayTeam"]


            home_rating = self.elo.get_rating(home)

            away_rating = self.elo.get_rating(away)


            prediction = self.predictor.predict(
                home_rating,
                away_rating
            )


            print(
                f"{home} vs {away}",
                prediction
            )


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