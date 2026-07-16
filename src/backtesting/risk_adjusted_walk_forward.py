from src.backtesting.backtester import Backtester

from src.betting.value_detector import ValueDetector
from src.betting.market_score_v2 import MarketScoreV2

from src.models.elo import EloRating
from src.models.elo_predictor import EloPredictor
from src.models.team_form import TeamForm

from src.betting.risk_adjusted_stake import (
    RiskAdjustedStake
)



class RiskAdjustedWalkForwardBacktester:


    def __init__(self):

        self.elo = EloRating()

        self.team_form = TeamForm()

        self.predictor = EloPredictor()

        self.value_detector = ValueDetector()

        self.market_score = MarketScoreV2()


        self.risk_stake = RiskAdjustedStake()

        self.backtester = Backtester()


        self.odds_min = None
        self.odds_max = None



    def check_odds(self, odds):

        if self.odds_min is None:
            return True

        return (
            self.odds_min <= odds <= self.odds_max
        )



    def check_market(
        self,
        odds,
        edge
    ):

        return self.market_score.is_valid(
            odds,
            edge
        )



    def run(
        self,
        df
    ):


        print(
            "Running Risk Adjusted Stake Walk Forward..."
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



            if (
                self.value_detector.is_value_bet(
                    home_value["edge"]
                )
                and
                self.check_odds(
                    match["HomeOdds"]
                )
                and
                self.check_market(
                    match["HomeOdds"],
                    home_value["edge"]
                )
            ):


                self.risk_stake.update_peak(
                    self.backtester.bankroll
                )


                self.backtester.stake = (
                    self.risk_stake.get_stake(
                        home_value["edge"],
                        self.backtester.bankroll
                    )
                )


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


                self.backtester.bets[-1]["market_score"] = (
                    self.market_score.calculate_score(
                        match["HomeOdds"],
                        home_value["edge"]
                    )
                )



            elif (
                self.value_detector.is_value_bet(
                    away_value["edge"]
                )
                and
                self.check_odds(
                    match["AwayOdds"]
                )
                and
                self.check_market(
                    match["AwayOdds"],
                    away_value["edge"]
                )
            ):


                self.risk_stake.update_peak(
                    self.backtester.bankroll
                )


                self.backtester.stake = (
                    self.risk_stake.get_stake(
                        away_value["edge"],
                        self.backtester.bankroll
                    )
                )


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

                self.backtester.bets[-1]["market_score"] = (
                    self.market_score.calculate_score(
                    match["AwayOdds"],
                    away_value["edge"]
                    )
                )


            result = (

                "H"
                if match["FTHG"] > match["FTAG"]

                else

                "A"
                if match["FTHG"] < match["FTAG"]

                else

                "D"

            )


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