import pandas as pd

from src.features.football_features import FootballFeatures

from src.backtesting.risk_adjusted_walk_forward import (
    RiskAdjustedWalkForwardBacktester
)


DATA_PATH = "data/raw"


SEASONS = {
    "2022_23": "premier_league_2022_23.csv",
    "2023_24": "premier_league_2023_24.csv",
    "2024_25": "premier_league_2024_25.csv",
}



def load_season(season):

    path = (
        f"{DATA_PATH}/"
        f"{SEASONS[season]}"
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



    frames = []


    for season in train_seasons:

        frames.append(
            load_season(season)
        )


    test_df = load_season(
        test_season
    )


    train_df = pd.concat(
        frames
    )


    full_df = pd.concat(
        [
            train_df,
            test_df
        ]
    )


    full_df = (
        full_df
        .sort_values(
            "Date"
        )
        .reset_index(
            drop=True
        )
    )


    backtester = (
        RiskAdjustedWalkForwardBacktester()
    )


    bets = backtester.run(
        full_df
    )


    test_year = (
        int(
            test_season[:4]
        )
        + 1
    )


    test_bets = [
        b
        for b in bets
        if b["date"].year == test_year
    ]



    wins = sum(
        1
        for b in test_bets
        if b["win"]
    )


    profit = sum(
        b["profit"]
        for b in test_bets
    )


    total_stake = sum(
        b["stake"]
        for b in test_bets
    )


    roi = (
        profit /
        total_stake *
        100
        if total_stake
        else 0
    )


    result = {

        "test": test_season,

        "bets": len(test_bets),

        "wins": wins,

        "profit": round(
            profit,
            2
        ),

        "roi": round(
            roi,
            2
        )
    }


    print(
        "FILTER RESULT:"
    )

    print(
        result
    )


    return result



def run():


    results = []


    results.append(
        run_test(
            [
                "2022_23"
            ],
            "2023_24"
        )
    )


    results.append(
        run_test(
            [
                "2022_23",
                "2023_24"
            ],
            "2024_25"
        )
    )


    print()

    print(
        "=" * 40
    )

    print(
        "FINAL OOS REPORT"
    )

    print(
        results
    )



if __name__ == "__main__":

    run()