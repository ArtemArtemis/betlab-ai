from src.models.elo import EloRating
from src.models.elo_predictor import EloPredictor
from src.backtesting.backtester import Backtester
from src.betting.value_detector import ValueDetector


class WalkForwardBacktester:

    def __init__(self):

        self.elo = EloRating()

        self.predictor = EloPredictor()

        self.backtester = Backtester()

        self.value_detector = ValueDetector()


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


            # Проверяем ставку на хозяев

            home_value = self.value_detector.calculate_edge(
                prediction["home_win"],
                match["HomeOdds"]
            )


            # Проверяем ставку на гостей

            away_value = self.value_detector.calculate_edge(
                prediction["away_win"],
                match["AwayOdds"]
            )


            if self.value_detector.is_value_bet(
                home_value["edge"]
            ):

                self.backtester.place_bet(
                    probability=prediction["home_win"],
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
                    probability=prediction["away_win"],
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


            # Определяем фактический результат

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


            # Обновляем Elo после матча

            self.elo.update(
                home,
                away,
                result,
                goal_difference
            )


        self.backtester.report()