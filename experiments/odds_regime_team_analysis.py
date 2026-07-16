import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(__file__)
    )
)

import pandas as pd

from src.features.football_features import FootballFeatures
from src.backtesting.risk_adjusted_walk_forward import (
    RiskAdjustedWalkForwardBacktester
)


SEASONS = [
    "2022_23",
    "2023_24",
    "2024_25"
]


MIN_ODDS = 3.0
MAX_ODDS = 6.0



def prepare_data(season):

    path = (
        f"data/raw/"
        f"premier_league_{season}.csv"
    )

    print(
        f"Loading {path}"
    )

    df = pd.read_csv(path)

    features = FootballFeatures(df)

    df = features.prepare()

    return df



def run():

    all_bets = []


    for season in SEASONS:

        print("=" * 30)
        print(season)
        print("=" * 30)


        df = prepare_data(
            season
        )


        backtester = (
            RiskAdjustedWalkForwardBacktester()
        )


        bets = backtester.run(
            df
        )


        for bet in bets:

            if (
                MIN_ODDS
                <=
                bet["odds"]
                <=
                MAX_ODDS
            ):

                bet["season"] = season

                all_bets.append(
                    bet
                )


    result = pd.DataFrame(
        all_bets
    )


    print("\nTEAM ANALYSIS")
    print("=" * 40)


    print(
        result.groupby(
            "home_team"
        )
        [
            "profit"
        ]
        .sum()
        .sort_values(
            ascending=False
        )
        .head(20)
    )


    print("\nLOSERS")
    print("=" * 40)


    print(
        result.groupby(
            "home_team"
        )
        [
            "profit"
        ]
        .sum()
        .sort_values()
        .head(20)
    )


    print("\nAWAY TEAMS")

    print(
        result.groupby(
            "away_team"
        )
        [
            "profit"
        ]
        .sum()
        .sort_values(
            ascending=False
        )
        .head(20)
    )



if __name__ == "__main__":

    run()