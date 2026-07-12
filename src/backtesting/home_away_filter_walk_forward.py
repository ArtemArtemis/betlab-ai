from src.models.elo import EloRating
from src.models.elo_predictor import EloPredictor

from src.models.team_form import TeamForm
from src.models.home_away_form import HomeAwayForm
from src.models.home_away_filter import HomeAwayFilter

from src.betting.value_detector import ValueDetector
from src.backtesting.backtester import Backtester



class HomeAwayFilterWalkForwardBacktester:


    def __init__(self):

        self.elo = EloRating()

        self.predictor = EloPredictor()

        self.team_form = TeamForm()

        self.home_away_form = HomeAwayForm()

        self.filter = HomeAwayFilter(
            min_form=0.5
        )

        self.value_detector = ValueDetector()

        self.backtester = Backtester()



    def run(self, df):

        print(
            "Running Home Away Filter Walk Forward Backtest..."
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


            home_edge = (
                self.value_detector.calculate_edge(
                    prediction["home_win"],
                    match["HomeOdds"]
                )
            )


            away_edge = (
                self.value_detector.calculate_edge(
                    prediction["away_win"],
                    match["AwayOdds"]
                )
            )


            home_form = (
                self.home_away_form.get_home_score(
                    home
                )
            )


            away_form = (
                self.home_away_form.get_away_score(
                    away
                )
            )



            if (
                self.value_detector.is_value_bet(
                    home_edge["edge"]
                )
                and
                self.filter.allow_home_bet(
                    home_form
                )
            ):

                result = (
                    "WIN"
                    if match["FTHG"] > match["FTAG"]
                    else "LOSS"
                )


                self.backtester.place_bet(
                    prediction["home_win"],
                    match["HomeOdds"],
                    result,
                    home,
                    away,
                    match["Date"]
                )



            elif (
                self.value_detector.is_value_bet(
                    away_edge["edge"]
                )
                and
                self.filter.allow_away_bet(
                    away_form
                )
            ):

                result = (
                    "WIN"
                    if match["FTAG"] > match["FTHG"]
                    else "LOSS"
                )


                self.backtester.place_bet(
                    prediction["away_win"],
                    match["AwayOdds"],
                    result,
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


            self.home_away_form.update(
                home,
                away,
                result
            )


        self.backtester.report()

        return self.backtester.bets