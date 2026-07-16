from src.models.elo import EloRating
from src.models.elo_predictor import EloPredictor
from src.models.team_form import TeamForm

from src.betting.value_detector import ValueDetector
from src.betting.risk_adjusted_stake import RiskAdjustedStake

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


THRESHOLDS = {

    "5_percent": 0.05,

    "7_percent": 0.07,

    "10_percent": 0.10,

    "12_percent": 0.12

}



class EdgeThresholdBacktest:


    def __init__(
        self,
        threshold
    ):

        self.threshold = threshold

        self.elo = EloRating()

        self.team_form = TeamForm()

        self.predictor = EloPredictor()

        self.value_detector = ValueDetector()

        self.stake_model = RiskAdjustedStake()

        self.bankroll = 1000

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


            candidates = []


            if match["HomeOdds"] > 1:

                candidates.append(

                    {

                        "side": "HOME",

                        "edge":
                            home_value["edge"],

                        "probability":
                            prediction["home_win"],

                        "odds":
                            match["HomeOdds"],

                        "win":
                            match["FTHG"] > match["FTAG"]

                    }

                )



            if match["AwayOdds"] > 1:

                candidates.append(

                    {

                        "side": "AWAY",

                        "edge":
                            away_value["edge"],

                        "probability":
                            prediction["away_win"],

                        "odds":
                            match["AwayOdds"],

                        "win":
                            match["FTAG"] > match["FTHG"]

                    }

                )



            if candidates:


                best = max(
                    candidates,
                    key=lambda x: x["edge"]
                )


                if best["edge"] >= self.threshold:


                    self.stake_model.update_peak(
                        self.bankroll
                    )


                    stake = (
                        self.stake_model.get_stake(
                            best["edge"],
                            self.bankroll
                        )
                    )


                    if best["win"]:

                        profit = (

                            stake *
                            (
                                best["odds"] - 1
                            )

                        )

                    else:

                        profit = -stake



                    self.bankroll += profit


                    self.bets.append(

                        {

                            "side":
                                best["side"],

                            "odds":
                                best["odds"],

                            "edge":
                                best["edge"],

                            "stake":
                                stake,

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

            x["profit"]

            for x in self.bets

        )


        total_stake = sum(

            x["stake"]

            for x in self.bets

        )


        roi = (

            profit / total_stake

            if total_stake

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
        "EDGE THRESHOLD OPTIMIZATION V2"
    )

    print(
        "=============================="
    )



    for name, threshold in THRESHOLDS.items():


        test = EdgeThresholdBacktest(
            threshold
        )


        for season, df in datasets.items():

            test.run(df)



        result = test.report()



        print(
            f"\n{name}"
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