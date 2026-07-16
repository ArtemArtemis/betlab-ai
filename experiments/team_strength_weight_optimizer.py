import pandas as pd

from src.features.football_features import FootballFeatures
from src.backtesting.risk_adjusted_walk_forward import (
    RiskAdjustedWalkForwardBacktester
)
from src.config.model_config import MODEL_CONFIG


SEASONS = [
    "2022_23",
    "2023_24",
    "2024_25"
]


WEIGHTS = [
    80,
    90,
    100
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

    df = features.prepare()

    return df



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
        "bets": len(bets),
        "wins": wins,
        "win_rate":
            round(
                wins / len(bets) * 100,
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
                * 100,
                2
            )
            if bets
            else 0
    }



def run():

    original_weight = (
        MODEL_CONFIG["strength_weight"]
    )


    results = []


    for weight in WEIGHTS:

        print("\n")
        print("="*30)
        print(
            "STRENGTH WEIGHT:",
            weight
        )
        print("="*30)


        MODEL_CONFIG[
            "strength_weight"
        ] = weight


        all_bets = []


        for season in SEASONS:

            df = load_season(
                season
            )


            backtester = (
                RiskAdjustedWalkForwardBacktester()
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
            "strength_weight"
        ] = weight


        results.append(
            result
        )


        print(
            result
        )


    MODEL_CONFIG[
        "strength_weight"
    ] = original_weight


    print("\n")
    print("==============================")
    print("FINAL OPTIMIZER RESULT")
    print("==============================")


    for r in sorted(
        results,
        key=lambda x: x["roi"],
        reverse=True
    ):

        print(r)



if __name__ == "__main__":
    run()