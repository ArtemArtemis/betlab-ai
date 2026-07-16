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



class MarketRegimeAnalyzer:


    def __init__(self):

        self.elo = EloRating()

        self.team_form = TeamForm()

        self.predictor = EloPredictor()

        self.value_detector = ValueDetector()

        self.bets = []



    def run(
        self,
        df,
        season
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



            candidates = [

                {
                    "side": "HOME",
                    "odds": match["HomeOdds"],
                    "edge": home_value["edge"],
                    "probability":
                        prediction["home_win"],
                    "win":
                        match["FTHG"] > match["FTAG"]
                },


                {
                    "side": "AWAY",
                    "odds": match["AwayOdds"],
                    "edge": away_value["edge"],
                    "probability":
                        prediction["away_win"],
                    "win":
                        match["FTAG"] > match["FTHG"]
                }

            ]



            bet = max(
                candidates,
                key=lambda x: x["edge"]
            )



            if bet["edge"] >= 0.07:


                profit = (

                    bet["odds"] - 1

                    if bet["win"]

                    else

                    -1

                )


                self.bets.append(

                    {

                        "season":
                            season,

                        "date":
                            match["Date"],

                        "month":
                            match["Date"].month,

                        "side":
                            bet["side"],

                        "odds":
                            bet["odds"],

                        "edge":
                            bet["edge"],

                        "probability":
                            bet["probability"],

                        "win":
                            bet["win"],

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



    def report_season(
        self,
        season
    ):


        data = [

            x for x in self.bets

            if x["season"] == season

        ]


        df = pd.DataFrame(data)


        print("\n==============================")

        print(
            f"SEASON {season}"
        )

        print("==============================")


        print(
            f"Bets: {len(df)}"
        )


        print(
            f"Wins: {df['win'].sum()}"
        )


        print(
            f"Win Rate: {df['win'].mean():.2%}"
        )


        print(
            f"Profit: {df['profit'].sum():+.2f}"
        )


        print(
            f"Avg Odds: {df['odds'].mean():.2f}"
        )


        print(
            f"Avg Edge: {df['edge'].mean():.2%}"
        )


        print("\nMONTHLY")


        monthly = (

            df.groupby("month")

            .agg(

                bets=("profit","count"),

                profit=("profit","sum"),

                roi=("profit","mean")

            )

        )


        print(
            monthly.round(2)
        )



if __name__ == "__main__":


    analyzer = MarketRegimeAnalyzer()


    datasets = {}


    for season, path in SEASONS.items():

        df = pd.read_csv(path)

        datasets[season] = (
            FootballFeatures(df).prepare()
        )



    for season, df in datasets.items():

        analyzer.run(
            df,
            season
        )


    for season in SEASONS.keys():

        analyzer.report_season(
            season
        )