import os
import pandas as pd


from src.features.football_features import FootballFeatures

from src.backtesting.risk_adjusted_walk_forward import (
    RiskAdjustedWalkForwardBacktester
)



DATA_PATH = "data/raw"



def prepare_data(season):

    filename = (
        f"premier_league_{season}.csv"
    )

    path = os.path.join(
        DATA_PATH,
        filename
    )


    if not os.path.exists(path):

        raise FileNotFoundError(
            f"Missing data file: {path}"
        )


    print(
        f"Loading: {path}"
    )


    df = pd.read_csv(
        path
    )


    features = FootballFeatures(
        df
    )


    df = features.prepare()


    return df



def run_test(
    season,
    odds_min,
    odds_max,
    name
):

    print()
    print("==============================")
    print(name)
    print("==============================")

    print(
        f"SEASON: {season}"
    )


    df = prepare_data(
        season
    )


    backtester = (
        RiskAdjustedWalkForwardBacktester()
    )


    bets = backtester.run(
        df
    )


    filtered = []


    for bet in bets:

        odds = bet["odds"]

        if (
            odds >= odds_min
            and odds <= odds_max
        ):

            filtered.append(
                bet
            )


    profit = sum(
        b["profit"]
        for b in filtered
    )


    stakes = sum(
        b["stake"]
        for b in filtered
    )


    roi = (
        profit / stakes * 100
        if stakes > 0
        else 0
    )


    wins = sum(
        1
        for b in filtered
        if b["win"]
    )


    print()

    print(
        f"Bets: {len(filtered)}"
    )

    print(
        f"Wins: {wins}"
    )

    print(
        f"Profit: {profit:+.2f}"
    )

    print(
        f"ROI: {roi:+.2f}%"
    )


    return filtered



if __name__ == "__main__":


    seasons = [
        "2022_23",
        "2023_24",
        "2024_25"
    ]


    for season in seasons:


        run_test(
            season,
            3.0,
            6.0,
            "ODDS RANGE TEST 3.0-6.0"
        )