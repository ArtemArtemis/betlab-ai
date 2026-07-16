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



def odds_bucket(odds):

    if odds < 4:
        return "3.0-4.0"

    elif odds < 5:
        return "4.0-5.0"

    else:
        return "5.0+"



def edge_bucket(edge):

    if edge < 0.09:
        return "0.07-0.09"

    elif edge < 0.12:
        return "0.09-0.12"

    else:
        return "0.12+"



def update_bucket(
    buckets,
    key,
    bet
):

    buckets[key]["bets"] += 1


    if bet["win"]:
        buckets[key]["wins"] += 1


    buckets[key]["profit"] += (
        bet["profit"]
    )



def calculate_report(
    buckets
):

    result = []


    for key, data in buckets.items():

        roi = (

            data["profit"]

            /

            (
                data["bets"]
                *
                10
            )

            *

            100

        )


        result.append(

            {

                "group":
                    key,

                "bets":
                    data["bets"],

                "wins":
                    data["wins"],

                "win_rate":
                    round(
                        data["wins"]
                        /
                        data["bets"]
                        *
                        100,
                        2
                    )
                    if data["bets"]
                    else 0,

                "profit":
                    round(
                        data["profit"],
                        2
                    ),

                "roi":
                    round(
                        roi,
                        2
                    )

            }

        )


    return sorted(
        result,
        key=lambda x: x["roi"],
        reverse=True
    )



def run():


    season_results = defaultdict(
        lambda:
        {
            "bets":0,
            "wins":0,
            "profit":0
        }
    )


    odds_results = defaultdict(
        lambda:
        {
            "bets":0,
            "wins":0,
            "profit":0
        }
    )


    edge_results = defaultdict(
        lambda:
        {
            "bets":0,
            "wins":0,
            "profit":0
        }
    )



    for season in SEASONS:


        print()
        print(
            "=" * 30
        )

        print(
            season
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



        for bet in bets:


            update_bucket(
                season_results,
                season,
                bet
            )


            update_bucket(
                odds_results,
                odds_bucket(
                    bet["odds"]
                ),
                bet
            )


            update_bucket(
                edge_results,
                edge_bucket(
                    bet["edge"]
                ),
                bet
            )



    print()
    print("==============================")
    print("SEASON STABILITY")
    print("==============================")


    for row in calculate_report(
        season_results
    ):

        print(row)



    print()
    print("==============================")
    print("ODDS STABILITY")
    print("==============================")


    for row in calculate_report(
        odds_results
    ):

        print(row)



    print()
    print("==============================")
    print("EDGE STABILITY")
    print("==============================")


    for row in calculate_report(
        edge_results
    ):

        print(row)



if __name__ == "__main__":
    run()