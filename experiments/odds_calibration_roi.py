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


CALIBRATION_FACTORS = [

    0.6,
    0.7,
    0.8,
    0.9

]


EDGE_THRESHOLD = 0.07



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



def generate_predictions(df):


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
                    match["FTAG"]

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
                    match["FTHG"]

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



def evaluate(
    predictions,
    factor
):


    bets = 0

    wins = 0

    profit = 0


    for p in predictions:


        probability = (

            p["probability"]
            *
            factor

        )


        market_probability = (

            1 /
            p["odds"]

        )


        edge = (

            probability
            -
            market_probability

        )


        if edge < EDGE_THRESHOLD:

            continue


        bets += 1


        if p["win"]:

            wins += 1

            profit += (
                p["odds"]
                -
                1
            )

        else:

            profit -= 1



    roi = (

        profit /
        bets
        *
        100

        if bets

        else 0

    )


    return {

        "factor":
            factor,

        "bets":
            bets,

        "wins":
            wins,

        "win_rate":
            round(
                wins /
                bets *
                100,
                2
            )
            if bets
            else 0,

        "profit":
            round(
                profit,
                2
            ),

        "roi":
            round(
                roi,
                2
            )

    }



def run():


    all_predictions = []


    for season in SEASONS:


        df = load_season(
            season
        )


        all_predictions.extend(

            generate_predictions(
                df
            )

        )



    print()

    print(
        "=============================="
    )

    print(
        "ODDS CALIBRATION ROI TEST"
    )

    print(
        "=============================="
    )


    for factor in CALIBRATION_FACTORS:


        result = evaluate(

            all_predictions,

            factor

        )


        print(
            result
        )



if __name__ == "__main__":

    run()