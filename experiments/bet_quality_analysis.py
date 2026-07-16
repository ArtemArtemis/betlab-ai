from src.models.elo import EloRating
from src.models.elo_predictor import EloPredictor
from src.models.team_form import TeamForm
from src.betting.value_detector import ValueDetector
from src.features.football_features import FootballFeatures

import pandas as pd


SEASONS = {

    "2022/23":
        "data/raw/premier_league_2022_23.csv",

    "2023/24":
        "data/raw/premier_league_2023_24.csv",

    "2024/25":
        "data/raw/premier_league_2024_25.csv"

}



class BetQualityAnalyzer:


    def __init__(self):

        self.elo = EloRating()

        self.team_form = TeamForm()

        self.predictor = EloPredictor()

        self.value_detector = ValueDetector()

        self.bets = []



    def run(
        self,
        df
    ):

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


            prediction = self.predictor.predict(
                home_rating,
                away_rating,
                form_difference
            )


            markets = [

                {
                    "side": "HOME",
                    "probability":
                        prediction["home_win"],
                    "odds":
                        match["HomeOdds"],
                    "win":
                        match["FTHG"] > match["FTAG"],
                    "team":
                        home
                },

                {
                    "side": "AWAY",
                    "probability":
                        prediction["away_win"],
                    "odds":
                        match["AwayOdds"],
                    "win":
                        match["FTAG"] > match["FTHG"],
                    "team":
                        away
                }

            ]


            for market in markets:

                value = (
                    self.value_detector.calculate_edge(
                        market["probability"],
                        market["odds"]
                    )
                )


                if self.value_detector.is_value_bet(
                    value["edge"]
                ):


                    profit = (

                        market["odds"] - 1

                        if market["win"]

                        else

                        -1

                    )


                    self.bets.append(

                        {
                            "side":
                                market["side"],

                            "team":
                                market["team"],

                            "odds":
                                market["odds"],

                            "edge":
                                value["edge"],

                            "profit":
                                profit
                        }

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



    def bucket_report(
        self,
        name,
        condition
    ):

        bets = [

            b for b in self.bets

            if condition(b)

        ]


        if not bets:

            return


        profit = sum(
            b["profit"]
            for b in bets
        )


        roi = (
            profit /
            len(bets)
        )


        print(
            f"\n{name}"
        )

        print(
            f"Bets: {len(bets)}"
        )

        print(
            f"Profit: {profit:+.2f}"
        )

        print(
            f"ROI: {roi:+.2%}"
        )



    def report(self):

        print(
            "\n=============================="
        )

        print(
            "BET QUALITY ANALYSIS"
        )

        print(
            "=============================="
        )


        self.bucket_report(
            "ODDS 1.20-2.00",
            lambda x:
            1.2 <= x["odds"] < 2
        )


        self.bucket_report(
            "ODDS 2.00-3.00",
            lambda x:
            2 <= x["odds"] < 3
        )


        self.bucket_report(
            "ODDS 3.00-5.00",
            lambda x:
            3 <= x["odds"] < 5
        )


        self.bucket_report(
            "ODDS 5+",
            lambda x:
            x["odds"] >= 5
        )


        self.bucket_report(
            "HOME",
            lambda x:
            x["side"] == "HOME"
        )


        self.bucket_report(
            "AWAY",
            lambda x:
            x["side"] == "AWAY"
        )


        self.bucket_report(
            "EDGE 7-10%",
            lambda x:
            0.07 <= x["edge"] < 0.10
        )


        self.bucket_report(
            "EDGE 10-15%",
            lambda x:
            0.10 <= x["edge"] < 0.15
        )


        self.bucket_report(
            "EDGE 15%+",
            lambda x:
            x["edge"] >= 0.15
        )



if __name__ == "__main__":


    analyzer = BetQualityAnalyzer()


    for season, path in SEASONS.items():

        df = pd.read_csv(path)

        df = FootballFeatures(df).prepare()

        analyzer.run(df)



    analyzer.report()