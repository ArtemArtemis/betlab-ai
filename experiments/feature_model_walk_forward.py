import pandas as pd


from src.features.football_features import FootballFeatures
from src.features.team_strength import TeamStrength

from src.models.elo import EloRating
from src.models.elo_predictor import EloPredictor
from src.models.team_form import TeamForm



SPLITS = [

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



def train(
    seasons
):


    elo = EloRating()

    form = TeamForm()

    strength = TeamStrength()



    for season in seasons:


        df = load_season(
            season
        )


        df = df.sort_values(
            by="Date"
        )


        for _,match in df.iterrows():


            strength.update(

                match["HomeTeam"],

                match["AwayTeam"],

                match["FTHG"],

                match["FTAG"]

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

                match["HomeTeam"],

                match["AwayTeam"],

                result,

                match["FTHG"] - match["FTAG"]

            )


            form.update(

                match["HomeTeam"],

                match["AwayTeam"],

                result

            )



    return elo, form, strength



def evaluate(

    df,

    elo,

    form,

    strength,

    use_strength=False

):


    predictor = EloPredictor()


    bets = 0

    wins = 0

    profit = 0



    df = df.sort_values(
        by="Date"
    )



    for _,match in df.iterrows():


        home = match["HomeTeam"]

        away = match["AwayTeam"]



        strength_difference = 0


        if use_strength:


            strength_difference = (

                strength.get_strength_difference(

                    home,

                    away

                )

            )



        prediction = predictor.predict(

            elo.get_rating(home),

            elo.get_rating(away),

            form.get_difference(

                home,

                away

            ),

            strength_difference

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



        for probability, odds, win in selections:


            edge = (

                probability

                -

                (1 / odds)

            )


            if edge < 0.07:

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


    for train_seasons,test_season in SPLITS:


        print()

        print(
            "=" * 30
        )

        print(
            "TRAIN:",
            train_seasons
        )

        print(
            "TEST:",
            test_season
        )


        elo,form,strength = train(
            train_seasons
        )


        test_df = load_season(
            test_season
        )


        print(
            "BASELINE ELO + FORM"
        )


        print(

            evaluate(

                test_df,

                elo,

                form,

                strength,

                False

            )

        )



        print(
            "WITH TEAM STRENGTH"
        )


        print(

            evaluate(

                test_df,

                elo,

                form,

                strength,

                True

            )

        )



if __name__ == "__main__":

    run()