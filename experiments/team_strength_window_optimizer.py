import pandas as pd

from src.features.football_features import FootballFeatures

from src.backtesting.risk_adjusted_walk_forward import (
    RiskAdjustedWalkForwardBacktester
)

from src.config.model_config import MODEL_CONFIG
from src.features.team_strength import TeamStrength



SEASONS = [
    "2022_23",
    "2023_24",
    "2024_25"
]


WINDOWS = [
    5,
    10,
    15,
    20
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


    original_window = 10


    results = []


    MODEL_CONFIG[
        "strength_weight"
    ] = 100



    for window in WINDOWS:


        print("\n")
        print("=" * 30)
        print(
            "WINDOW:",
            window
        )
        print("=" * 30)



        all_bets = []



        for season in SEASONS:


            df = load_season(
                season
            )


            backtester = (
                RiskAdjustedWalkForwardBacktester()
            )


            backtester.team_strength = (
                TeamStrength(
                    window=window
                )
            )


            bets = backtester.run(
                df
            )


            all_bets.extend(
                bets
            )



        result = calculate_result(
            all_bets
        )


        result[
            "window"
        ] = window


        results.append(
            result
        )


        print(
            result
        )



    print("\n")
    print("==============================")
    print(
        "FINAL TEAM STRENGTH WINDOW OPTIMIZER"
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