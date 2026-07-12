from src.models.elo import EloRating
from src.models.home_away_predictor import HomeAwayPredictor
from src.models.home_away_form import HomeAwayForm
from src.backtesting.backtester import Backtester
from src.betting.value_detector import ValueDetector



class HomeAwayWalkForwardBacktester:


    def __init__(self):

        self.elo = EloRating()

        self.home_away_form = HomeAwayForm()

        self.predictor = HomeAwayPredictor()

        self.backtester = Backtester()

        self.value_detector = ValueDetector()



    def run(
        self,
        df
    ):

        print(
            "Running Home Away Walk Forward Backtest..."
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
                self.home_away_form.get_difference(
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

                result = (
                    "WIN"
                    if match["FTHG"] > match["FTAG"]
                    else "LOSS"
                )


                self.backtester.place_bet(
                    probability=prediction["home_win"],
                    odds=match["HomeOdds"],
                    result=result,
                    home_team=home,
                    away_team=away,
                    date=match["Date"]
                )


            elif self.value_detector.is_value_bet(
                away_value["edge"]
            ):

                result = (
                    "WIN"
                    if match["FTAG"] > match["FTHG"]
                    else "LOSS"
                )


                self.backtester.place_bet(
                    probability=prediction["away_win"],
                    odds=match["AwayOdds"],
                    result=result,
                    home_team=home,
                    away_team=away,
                    date=match["Date"]
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


            self.home_away_form.update(
                home,
                away,
                result
            )


        self.backtester.report()


        return self.backtester.bets