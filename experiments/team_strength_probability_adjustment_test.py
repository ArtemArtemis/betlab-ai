import pandas as pd


from src.features.football_features import FootballFeatures

from src.models.elo import EloRating
from src.models.team_form import TeamForm
from src.models.elo_predictor import EloPredictor

from src.features.team_strength import TeamStrength

from src.config.model_config import MODEL_CONFIG



SEASONS = [
    "2022_23",
    "2023_24",
    "2024_25"
]


STRENGTH_FACTORS = [
    0.0,
    0.25,
    0.5,
    0.75,
    1.0
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



def calculate_result(bets):

    profit = sum(
        b["profit"]
        for b in bets
    )

    wins = sum(
        1
        for b in bets
        if b["win"]
    )


    return {

        "bets":
            len(bets),

        "wins":
            wins,

        "win_rate":
            round(
                wins /
                len(bets)
                *
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
                profit /
                (len(bets) * 10)
                *
                100,
                2
            )
            if bets
            else 0

    }



def run_model(
    df,
    strength_factor
):


    elo = EloRating()

    form = TeamForm()

    predictor = EloPredictor()

    strength = TeamStrength(
        window=10
    )



    bets = []



    df = df.sort_values(
        by="Date"
    )



    for _, match in df.iterrows():


        home = match["HomeTeam"]

        away = match["AwayTeam"]



        home_rating = elo.get_rating(
            home
        )

        away_rating = elo.get_rating(
            away
        )



        form_difference = (
            form.get_difference(
                home,
                away
            )
        )



        strength_difference = (
            strength.get_strength_difference(
                home,
                away
            )
        )



        adjusted_strength = (
            strength_difference
            *
            strength_factor
        )



        prediction = predictor.predict(
            home_rating,
            away_rating,
            form_difference,
            adjusted_strength
        )



        probability = (
            prediction["home_win"]
        )


        odds = match["HomeOdds"]


        edge = (
            probability
            -
            (
                1 / odds
            )
        )


        if edge >= 0.07:


            win = (
                match["FTHG"]
                >
                match["FTAG"]
            )


            profit = (

                odds * 10 - 10

                if win

                else

                -10

            )


            bets.append(

                {

                    "win":
                        win,

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


        strength.update(
            home,
            away,
            match["FTHG"],
            match["FTAG"]
        )



    return bets



def run():


    MODEL_CONFIG[
        "strength_weight"
    ] = 100



    results = []



    for factor in STRENGTH_FACTORS:


        all_bets = []



        print()
        print(
            "FACTOR:",
            factor
        )


        for season in SEASONS:


            df = load_season(
                season
            )


            bets = run_model(
                df,
                factor
            )


            all_bets.extend(
                bets
            )



        result = calculate_result(
            all_bets
        )


        result[
            "strength_factor"
        ] = factor


        results.append(
            result
        )


        print(
            result
        )



    print()
    print("==============================")
    print(
        "FINAL TEAM STRENGTH ADJUSTMENT"
    )
    print("==============================")


    for result in sorted(
        results,
        key=lambda x: x["roi"],
        reverse=True
    ):

        print(result)



if __name__ == "__main__":
    run()