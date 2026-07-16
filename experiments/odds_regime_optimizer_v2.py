import itertools

from collections import defaultdict

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


ODDS_REGIMES = {

    "3.0-4.0":
        (3.0, 4.0),

    "4.0-5.0":
        (4.0, 5.0),

    "5.0+":
        (5.0, 99.0)

}


EDGE_VALUES = [
    0.06,
    0.07,
    0.08,
    0.09,
    0.10,
    0.12
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



def get_regime(odds):

    for name, values in ODDS_REGIMES.items():

        if values[0] <= odds < values[1]:

            return name


    return None



def calculate_report(
    bets
):

    profit = sum(
        bet["profit"]
        for bet in bets
    )


    wins = sum(
        1
        for bet in bets
        if bet["win"]
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
                (
                    len(bets)
                    *
                    10
                )
                *
                100,
                2
            )
            if bets
            else 0

    }



def run():


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



    prepared = []



    for bet in all_bets:


        regime = get_regime(
            bet["odds"]
        )


        if regime:

            prepared.append(
                {

                    "regime":
                        regime,

                    "edge":
                        bet["edge"],

                    "bet":
                        bet

                }
            )



    results = []



    for combination in itertools.product(
        EDGE_VALUES,
        repeat=3
    ):


        filters = dict(

            zip(
                ODDS_REGIMES.keys(),
                combination
            )

        )


        selected = []



        for item in prepared:


            if (
                item["edge"]
                >=
                filters[
                    item["regime"]
                ]
            ):

                selected.append(
                    item["bet"]
                )



        report = calculate_report(
            selected
        )


        report[
            "filters"
        ] = filters


        results.append(
            report
        )



    print()
    print("==============================")
    print(
        "FINAL ODDS REGIME OPTIMIZER"
    )
    print("==============================")


    for result in sorted(
        results,
        key=lambda x: x["roi"],
        reverse=True
    )[:10]:

        print(result)



if __name__ == "__main__":
    run()