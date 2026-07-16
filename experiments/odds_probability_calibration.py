import pandas as pd
from collections import defaultdict


from src.features.football_features import FootballFeatures

from src.models.elo import EloRating
from src.models.elo_predictor import EloPredictor
from src.models.team_form import TeamForm



SEASONS = [
    "2022_23",
    "2023_24",
    "2024_25"
]



ODDS_BUCKETS = [

    ("1.5-2.5", 1.5, 2.5),

    ("2.5-3.5", 2.5, 3.5),

    ("3.5-5.0", 3.5, 5.0),

    ("5.0+", 5.0, 100)

]



def load_season(season):

    path = (
        f"data/raw/premier_league_{season}.csv"
    )


    print(
        f"Loading {path}"
    )


    df = pd.read_csv(
        path,
        encoding="utf-8"
    )


    features = FootballFeatures(
        df
    )


    return features.prepare()



def run_model(df):


    elo = EloRating()

    form = TeamForm()

    predictor = EloPredictor()


    predictions = []


    df = df.sort_values(
        by="Date"
    )


    for _, match in df.iterrows():


        home = match["HomeTeam"]

        away = match["AwayTeam"]


        home_rating = (
            elo.get_rating(home)
        )

        away_rating = (
            elo.get_rating(away)
        )


        form_difference = (
            form.get_difference(
                home,
                away
            )
        )


        prediction = (
            predictor.predict(
                home_rating,
                away_rating,
                form_difference
            )
        )


        predictions.append(

            {

                "odds":
                    match["HomeOdds"],

                "probability":
                    prediction["home_win"],

                "win":
                    match["FTHG"]
                    >
                    match["FTAG"],

                "side":
                    "HOME"

            }

        )


        predictions.append(

            {

                "odds":
                    match["AwayOdds"],

                "probability":
                    prediction["away_win"],

                "win":
                    match["FTAG"]
                    >
                    match["FTHG"],

                "side":
                    "AWAY"

            }

        )


        result = (

            "H"
            if match["FTHG"] > match["FTAG"]

            else

            "A"
            if match["FTAG"] > match["FTHG"]

            else

            "D"

        )


        elo.update(

            home,

            away,

            result,

            match["FTHG"] - match["FTAG"]

        )


        form.update(

            home,

            away,

            result

        )


    return predictions



def analyze(predictions):


    buckets = defaultdict(

        lambda: {

            "bets":0,

            "wins":0,

            "prob_sum":0

        }

    )


    for p in predictions:


        for name, low, high in ODDS_BUCKETS:


            if low <= p["odds"] < high:


                data = buckets[name]


                data["bets"] += 1


                data["wins"] += (
                    1
                    if p["win"]
                    else 0
                )


                data["prob_sum"] += (
                    p["probability"]
                )


                break



    print()

    print(
        "=============================="
    )

    print(
        "ODDS PROBABILITY CALIBRATION"
    )

    print(
        "=============================="
    )


    for bucket,data in buckets.items():


        actual = (

            data["wins"]
            /
            data["bets"]
            *
            100

            if data["bets"]

            else 0

        )


        predicted = (

            data["prob_sum"]
            /
            data["bets"]
            *
            100

            if data["bets"]

            else 0

        )


        error = (
            predicted
            -
            actual
        )


        print(

            {

                "odds":
                    bucket,

                "bets":
                    data["bets"],

                "predicted":
                    round(
                        predicted,
                        2
                    ),

                "actual":
                    round(
                        actual,
                        2
                    ),

                "error":
                    round(
                        error,
                        2
                    )

            }

        )



def run():


    all_predictions = []


    for season in SEASONS:


        df = load_season(
            season
        )


        predictions = run_model(
            df
        )


        all_predictions.extend(
            predictions
        )


    analyze(
        all_predictions
    )



if __name__ == "__main__":

    run()