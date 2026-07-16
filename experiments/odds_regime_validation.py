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



ODDS_MIN=3.0
ODDS_MAX=6.0



def load(season):

    path=(
        f"data/raw/"
        f"premier_league_{season}.csv"
    )


    df=pd.read_csv(
        path
    )


    return FootballFeatures(
        df
    ).prepare()



def test(
    train,
    test
):

    print("="*40)
    print(
        f"TRAIN {train}"
    )
    print(
        f"TEST {test}"
    )
    print("="*40)



    train_df=load(
        train
    )


    test_df=load(
        test
    )


    model=(
        RiskAdjustedWalkForwardBacktester()
    )


    # прогоняем train
    model.run(
        train_df
    )


    # новый тестовый период
    result=model.run(
        test_df
    )


    bets=[]


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


    profit=sum(
        x["profit"]
        for x in bets
    )


    print(
        "BETS:",
        len(bets)
    )

    print(
        "PROFIT:",
        round(
            profit,
            2
        )
    )



if __name__=="__main__":


    test(
        "2022_23",
        "2023_24"
    )


    test(
        "2022_23",
        "2024_25"
    )