import pandas as pd


from src.features.football_features import FootballFeatures

from src.models.elo import EloRating
from src.models.elo_predictor import EloPredictor
from src.models.team_form import TeamForm

from src.models.probability_calibration import (
    ProbabilityCalibration
)



TRAIN_TEST_SPLITS = [

    (
        ["2022_23"],
        "2023_24"
    ),

    (
        [
            "2022_23",
            "2023_24"
        ],
        "2024_25"
    )

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



def train_model(
    seasons
):


    elo = EloRating()

    form = TeamForm()

    predictor = EloPredictor()



    for season in seasons:


        df = load_season(
            season
        )


        df = df.sort_values(
            by="Date"
        )


        for _,match in df.iterrows():


            home = match["HomeTeam"]

            away = match["AwayTeam"]


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



    return (
        elo,
        form,
        EloPredictor()
    )



def test_model(
    df,
    elo,
    form,
    predictor
):


    calibration = ProbabilityCalibration()


    bets = 0

    wins = 0

    profit = 0



    df = df.sort_values(
        by="Date"
    )



    for _,match in df.iterrows():


        home = match["HomeTeam"]

        away = match["AwayTeam"]


        prediction = predictor.predict(

            elo.get_rating(home),

            elo.get_rating(away),

            form.get_difference(
                home,
                away
            )

        )


        selections = [

            (
                prediction["home_win"],
                match["HomeOdds"],
                match["FTHG"] > match["FTAG"]
            ),

            (
                prediction["away_win"],
                match["AwayOdds"],
                match["FTAG"] > match["FTHG"]
            )

        ]



        for probability,odds,win in selections:


            calibrated = calibration.calibrate(

                probability,

                odds

            )


            calibrated_probability = (

                calibrated[
                    "calibrated_probability"
                ]

            )


            market_probability = (

                1 / odds

            )


            edge = (

                calibrated_probability
                -
                market_probability

            )


            if edge < EDGE_THRESHOLD:

                continue



            bets += 1


            if win:

                wins += 1

                profit += (
                    odds - 1
                )

            else:

                profit -= 1



    return {

        "bets":
            bets,

        "wins":
            wins,

        "win_rate":
            round(
                wins / bets * 100,
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
                profit / bets * 100,
                2
            )
            if bets
            else 0

    }



def run():


    for train_seasons,test_season in TRAIN_TEST_SPLITS:


        print()
        print("="*30)

        print(
            "TRAIN:",
            train_seasons
        )

        print(
            "TEST:",
            test_season
        )



        elo,form,predictor = train_model(
            train_seasons
        )


        test_df = load_season(
            test_season
        )


        result = test_model(

            test_df,

            elo,

            form,

            predictor

        )


        print(
            result
        )



if __name__ == "__main__":

    run()