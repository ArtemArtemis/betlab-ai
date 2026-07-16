from src.features.football_features import FootballFeatures

from src.backtesting.risk_adjusted_walk_forward import (
    RiskAdjustedWalkForwardBacktester
)

from src.evaluation.stability_checker import (
    StabilityChecker
)

from src.evaluation.confidence_report import (
    ConfidenceReport
)

import pandas as pd



SEASONS = [

    "2022_23",

    "2023_24",

    "2024_25"

]



def load_season(
    season
):

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


    return features.prepare()



def run():


    checker = StabilityChecker()


    for season in SEASONS:


        print(
            "\n=============================="
        )

        print(
            season
        )

        print(
            "=============================="
        )


        df = load_season(
            season
        )


        backtester = (
            RiskAdjustedWalkForwardBacktester()
        )


        bets = backtester.run(
            df
        )


        profit = sum(
            x["profit"]
            for x in bets
        )


        wins = sum(
            1
            for x in bets
            if x["win"]
        )


        roi = (

            profit /
            (len(bets) * 10)
            *
            100

        )


        checker.add_result(

            season,

            len(bets),

            wins,

            profit,

            roi

        )


    result = checker.summary()


    ConfidenceReport().generate(
        result
    )



if __name__ == "__main__":

    run()