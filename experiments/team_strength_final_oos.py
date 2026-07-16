import pandas as pd

from src.features.football_features import FootballFeatures

from src.backtesting.risk_adjusted_walk_forward import (
    RiskAdjustedWalkForwardBacktester
)

from src.config.model_config import MODEL_CONFIG



WEIGHTS = [
    80,
    90,
    100
]


TESTS = [

    {
        "train": [
            "2022_23"
        ],
        "test": "2023_24"
    },


    {
        "train": [
            "2022_23",
            "2023_24"
        ],
        "test": "2024_25"
    }

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



def run():


    original = MODEL_CONFIG[
        "strength_weight"
    ]


    results = []


    for weight in WEIGHTS:


        MODEL_CONFIG[
            "strength_weight"
        ] = weight


        print("\n")
        print("="*30)
        print(
            "WEIGHT:",
            weight
        )
        print("="*30)



        for test in TESTS:


            print(
                "TRAIN:",
                test["train"]
            )


            print(
                "TEST:",
                test["test"]
            )


            for season in test["train"]:

                load_season(
                    season
                )



            df = load_season(
                test["test"]
            )



            backtester = (
                RiskAdjustedWalkForwardBacktester()
            )


            bets = backtester.run(
                df
            )



            result = calculate_result(
                bets
            )


            result[
                "weight"
            ] = weight


            result[
                "test"
            ] = test["test"]


            results.append(
                result
            )


            print(
                result
            )



    MODEL_CONFIG[
        "strength_weight"
    ] = original



    print("\n")
    print("==============================")
    print("FINAL TEAM STRENGTH FINAL OOS")
    print("==============================")


    for r in results:

        print(r)



if __name__ == "__main__":
    run()