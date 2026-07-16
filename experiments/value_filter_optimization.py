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



class ValueFilterOptimizer:


    def __init__(
        self,
        variant
    ):

        self.variant = variant

        self.elo = EloRating()

        self.team_form = TeamForm()

        self.predictor = EloPredictor()

        self.value_detector = ValueDetector()

        self.bets = []



    def filter_bet(
        self,
        side,
        odds,
        edge
    ):


        if self.variant == "A":

            # Odds filter

            return (
                1.2 <= odds <= 3.0
            )


        if self.variant == "B":

            # Edge filter

            return (
                edge >= 0.10
            )


        if self.variant == "C":

            # Combined

            return (

                side == "HOME"

                and

                1.2 <= odds <= 3.0

                and

                edge >= 0.10

            )


        if self.variant == "D":

            # Conservative value zone

            return (

                side == "HOME"

                and

                2.0 <= odds <= 3.0

                and

                edge >= 0.10

            )


        return False



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



            markets = [

                {

                    "side": "HOME",

                    "odds":
                        match["HomeOdds"],

                    "probability":
                        prediction["home_win"],

                    "win":
                        match["FTHG"] > match["FTAG"]

                },


                {

                    "side": "AWAY",

                    "odds":
                        match["AwayOdds"],

                    "probability":
                        prediction["away_win"],

                    "win":
                        match["FTAG"] > match["FTHG"]

                }

            ]



            for market in markets:


                value = (
                    self.value_detector.calculate_edge(
                        market["probability"],
                        market["odds"]
                    )
                )


                edge = value["edge"]


                if self.filter_bet(

                    market["side"],

                    market["odds"],

                    edge

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

                            "odds":
                                market["odds"],

                            "edge":
                                edge,

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



    def report(self):

        bets = len(
            self.bets
        )


        profit = sum(

            b["profit"]

            for b in self.bets

        )


        roi = (

            profit / bets

            if bets

            else 0

        )


        return {

            "bets":
                bets,

            "profit":
                round(
                    profit,
                    2
                ),

            "roi":
                round(
                    roi * 100,
                    2
                )

        }



if __name__ == "__main__":


    datasets = {}


    for season, path in SEASONS.items():

        df = pd.read_csv(path)

        datasets[season] = (
            FootballFeatures(df).prepare()
        )



    print(
        "\n=============================="
    )

    print(
        "VALUE FILTER OPTIMIZATION"
    )

    print(
        "=============================="
    )



    for variant in [
        "A",
        "B",
        "C",
        "D"
    ]:


        analyzer = ValueFilterOptimizer(
            variant
        )


        for season, df in datasets.items():

            analyzer.run(df)



        result = analyzer.report()



        print(
            f"\nVariant {variant}"
        )

        print(
            f"Bets: {result['bets']}"
        )

        print(
            f"Profit: {result['profit']:+.2f}"
        )

        print(
            f"ROI: {result['roi']:+.2f}%"
        )