from src.models.elo import EloRating
from src.models.elo_predictor import EloPredictor
from src.models.team_form import TeamForm

from src.models.draw_risk_detector import DrawRiskDetector

from src.betting.value_detector import ValueDetector
from src.backtesting.backtester import Backtester



class DrawRiskWalkForwardBacktester:


    def __init__(self):

        self.elo = EloRating()

        self.predictor = EloPredictor()

        self.team_form = TeamForm()

        self.draw_detector = DrawRiskDetector()

        self.value_detector = ValueDetector()

        self.backtester = Backtester()



    def run(self, df):

        print(
            "Running Draw Risk Walk Forward Backtest..."
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


            form_difference = (
                self.team_form.get_difference(
                    home,
                    away
                )
            )


            risky_draw = (
                self.draw_detector.high_risk(
                    home_rating,
                    away_rating,
                    form_difference
                )
            )


            if risky_draw:

                allow_bet = False

            else:

                allow_bet = True



            if allow_bet:


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


                if self.value_detector.is_value_bet(
                    home_edge["edge"]
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


                elif self.value_detector.is_value_bet(
                    away_edge["edge"]
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



            # update models

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