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



class ValueBucketAnalyzer:


    def __init__(self):

        self.elo = EloRating()

        self.team_form = TeamForm()

        self.predictor = EloPredictor()

        self.value_detector = ValueDetector()

        self.bets = []



    def run(self, df):

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


            prediction = (
                self.predictor.predict(
                    home_rating,
                    away_rating,
                    form_difference
                )
            )


            outcomes = [

                {
                    "side": "HOME",
                    "probability":
                        prediction["home_win"],
                    "odds":
                        match["HomeOdds"]
                },

                {
                    "side": "AWAY",
                    "probability":
                        prediction["away_win"],
                    "odds":
                        match["AwayOdds"]
                }

            ]


            for outcome in outcomes:

                edge_data = (
                    self.value_detector.calculate_edge(
                        outcome["probability"],
                        outcome["odds"]
                    )
                )


                edge = edge_data["edge"]


                if edge >= 0.05:


                    win = False


                    if outcome["side"] == "HOME":

                        win = (
                            match["FTHG"]
                            >
                            match["FTAG"]
                        )


                    if outcome["side"] == "AWAY":

                        win = (
                            match["FTAG"]
                            >
                            match["FTHG"]
                        )


                    profit = (

                        outcome["odds"] - 1

                        if win

                        else

                        -1

                    )


                    self.bets.append(

                        {
                            "edge": edge,
                            "odds": outcome["odds"],
                            "win": win,
                            "profit": profit
                        }

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



    def report(self):

        buckets = {

            "5-7%": [],
            "7-10%": [],
            "10-15%": [],
            "15%+": []

        }


        for bet in self.bets:

            edge = bet["edge"]


            if edge < 0.07:

                buckets["5-7%"].append(bet)


            elif edge < 0.10:

                buckets["7-10%"].append(bet)


            elif edge < 0.15:

                buckets["10-15%"].append(bet)


            else:

                buckets["15%+"].append(bet)



        print(
            "\n=============================="
        )

        print(
            "VALUE BUCKET ANALYSIS"
        )

        print(
            "=============================="
        )


        for name, bets in buckets.items():

            if len(bets) == 0:

                continue


            profit = sum(
                b["profit"]
                for b in bets
            )


            stake = len(bets)


            roi = (
                profit / stake
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



if __name__ == "__main__":


    analyzer = ValueBucketAnalyzer()


    for season, path in SEASONS.items():

        print(
            f"\nRunning {season}"
        )


        df = pd.read_csv(path)

        df = FootballFeatures(df).prepare()

        analyzer.run(df)



    analyzer.report()