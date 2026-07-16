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


ODDS_MIN = 3.0
ODDS_MAX = 6.0



def prepare(season):

    path = (
        f"data/raw/"
        f"premier_league_{season}.csv"
    )

    df = pd.read_csv(
        path
    )

    features = FootballFeatures(
        df
    )

    return features.prepare()



def run():

    bets=[]


    for season in SEASONS:


        print(
            season
        )


        df = prepare(
            season
        )


        engine = (
            RiskAdjustedWalkForwardBacktester()
        )


        result = engine.run(
            df
        )


        for bet in result:

            if (
                ODDS_MIN
                <=
                bet["odds"]
                <=
                ODDS_MAX
            ):

                bets.append(
                    bet
                )



    df = pd.DataFrame(
        bets
    )


    bins=[
        0.07,
        0.08,
        0.09,
        0.10,
        0.11,
        1
    ]


    labels=[
        "7-8",
        "8-9",
        "9-10",
        "10-11",
        "11+"
    ]


    df["edge_bucket"]=pd.cut(
        df["edge"],
        bins=bins,
        labels=labels
    )


    print(
        df.groupby(
            "edge_bucket",
            observed=True
        )
        .agg(
            bets=("profit","count"),
            profit=("profit","sum")
        )
    )



if __name__=="__main__":

    run()