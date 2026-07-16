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


FILTERS = {

    "A_ODDS_3_6_EDGE_8_10": {
        "min_odds": 3.0,
        "max_odds": 6.0,
        "min_edge": 0.08,
        "max_edge": 0.10
    },


    "B_ODDS_3_6_EDGE_9_10": {
        "min_odds": 3.0,
        "max_odds": 6.0,
        "min_edge": 0.09,
        "max_edge": 0.10
    },


    "C_ODDS_3_6_EDGE_9_11": {
        "min_odds": 3.0,
        "max_odds": 6.0,
        "min_edge": 0.09,
        "max_edge": 0.11
    },


    "D_ODDS_2_5_6_EDGE_9_10": {
        "min_odds": 2.5,
        "max_odds": 6.0,
        "min_edge": 0.09,
        "max_edge": 0.10
    }

}



def load_data(
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



def run_filter(
    bets,
    config
):

    filtered = []


    for bet in bets:


        if (
            config["min_odds"]
            <=
            bet["odds"]
            <=
            config["max_odds"]
        ):

            if (
                config["min_edge"]
                <=
                bet["edge"]
                <=
                config["max_edge"]
            ):

                filtered.append(
                    bet
                )


    return filtered



def analyze(
    bets
):

    if len(bets)==0:

        return {
            "bets":0,
            "wins":0,
            "profit":0,
            "roi":0
        }


    profit = sum(
        x["profit"]
        for x in bets
    )


    wins = sum(
        1
        for x in bets
        if x["win"]
    )


    total_stake = sum(
        x["stake"]
        for x in bets
    )


    roi = (
        profit /
        total_stake *
        100
    )


    return {

        "bets": len(bets),

        "wins": wins,

        "win_rate":
            round(
                wins /
                len(bets)
                *
                100,
                2
            ),

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



def run():


    print(
        "="*40
    )

    print(
        "FINAL ODDS REGIME FILTER TEST"
    )

    print(
        "="*40
    )


    all_results=[]



    for name, config in FILTERS.items():


        print(
            "\n"
            +
            "="*40
        )

        print(
            name
        )

        print(
            "="*40
        )


        total=[]



        for season in SEASONS:


            df = load_data(
                season
            )


            model = (
                RiskAdjustedWalkForwardBacktester()
            )


            bets = model.run(
                df
            )


            filtered = run_filter(
                bets,
                config
            )


            result = analyze(
                filtered
            )


            print(
                season
            )

            print(
                result
            )


            total.extend(
                filtered
            )



        final = analyze(
            total
        )


        print(
            "\nTOTAL"
        )

        print(
            final
        )


        all_results.append(
            {
                "filter":name,
                **final
            }
        )



    print(
        "\n\nLEADERBOARD"
    )

    print(
        pd.DataFrame(
            all_results
        )
        .sort_values(
            by="roi",
            ascending=False
        )
    )



if __name__=="__main__":

    run()