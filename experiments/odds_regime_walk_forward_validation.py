import pandas as pd

from src.features.football_features import FootballFeatures
from src.backtesting.risk_adjusted_walk_forward import (
    RiskAdjustedWalkForwardBacktester
)


SEASONS = [
    "2022_23",
    "2023_24",
    "2024_25",
]


ODDS_MIN = 3.0
ODDS_MAX = 6.0

EDGE_MIN = 0.09
EDGE_MAX = 0.10



def load_features(season):

    path = (
        f"data/raw/"
        f"premier_league_{season}.csv"
    )

    print(
        f"Loading {path}"
    )

    df = pd.read_csv(
        path
    )

    features = FootballFeatures(
        df
    )

    df = features.prepare()

    return df



def apply_filter(
    bets
):

    filtered = []

    for bet in bets:

        odds = bet["odds"]

        edge = bet["edge"]

        if (
            ODDS_MIN <= odds <= ODDS_MAX
            and
            EDGE_MIN <= edge <= EDGE_MAX
        ):

            filtered.append(
                bet
            )

    return filtered



def calculate_result(
    bets
):

    profit = sum(
        bet["profit"]
        for bet in bets
    )

    count = len(
        bets
    )

    wins = sum(
        1
        for bet in bets
        if bet["win"]
    )

    roi = (
        profit / 
        sum(
            bet["stake"]
            for bet in bets
        )
        *
        100
        if count
        else 0
    )

    return {

        "bets": count,

        "wins": wins,

        "win_rate":
            round(
                wins / count * 100,
                2
            )
            if count
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



def run_test(
    train_seasons,
    test_season
):


    print("=" * 40)

    print(
        "TRAIN:",
        train_seasons
    )

    print(
        "TEST:",
        test_season
    )

    print("=" * 40)



    train_df = pd.concat(
        [
            load_features(
                season
            )
            for season in train_seasons
        ]
    )


    test_df = load_features(
        test_season
    )



    model = RiskAdjustedWalkForwardBacktester()



    model.run(
        train_df
    )


    test_model = RiskAdjustedWalkForwardBacktester()


    bets = test_model.run(
        test_df
    )


    filtered = apply_filter(
        bets
    )


    result = calculate_result(
        filtered
    )


    print(
        "FILTER RESULT:"
    )

    print(
        result
    )



if __name__ == "__main__":


    run_test(
        [
            "2022_23"
        ],
        "2023_24"
    )


    run_test(
        [
            "2022_23",
            "2023_24"
        ],
        "2024_25"
    )