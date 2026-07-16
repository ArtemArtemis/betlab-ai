from src.backtesting.risk_adjusted_walk_forward import (
    RiskAdjustedWalkForwardBacktester
)

from src.features.football_features import FootballFeatures

import pandas as pd


SEASONS = {

    "2022/23":
        "data/raw/premier_league_2022_23.csv",

    "2023/24":
        "data/raw/premier_league_2023_24.csv",

    "2024/25":
        "data/raw/premier_league_2024_25.csv"

}



ODDS_BUCKETS = {

    "3.0-4.0":
        (3.0, 4.0),

    "4.0-5.0":
        (4.0, 5.0),

    "5.0-6.0":
        (5.0, 6.0)

}



def prepare_data(path):

    df = pd.read_csv(path)

    return FootballFeatures(df).prepare()



def filter_odds(
    bets,
    minimum,
    maximum
):

    return [

        bet

        for bet in bets

        if minimum <= bet["odds"] < maximum

    ]



def calculate_result(bets):


    if not bets:

        return {
            "bets": 0,
            "wins": 0,
            "profit": 0,
            "roi": 0
        }



    profit = sum(
        bet["profit"]
        for bet in bets
    )


    stake = sum(
        bet["stake"]
        for bet in bets
    )


    wins = sum(
        1
        for bet in bets
        if bet["win"]
    )


    roi = (

        profit / stake * 100

        if stake > 0

        else 0

    )


    return {

        "bets":
            len(bets),

        "wins":
            wins,

        "profit":
            round(profit, 2),

        "roi":
            round(roi, 2)

    }



if __name__ == "__main__":


    print()

    print("==============================")

    print("ODDS RANGE BREAKDOWN")

    print("==============================")



    datasets = {}


    for season, path in SEASONS.items():

        datasets[season] = prepare_data(path)



    for bucket, odds in ODDS_BUCKETS.items():


        print()

        print("==============================")

        print(bucket)

        print("==============================")


        total_bets = []


        for season, df in datasets.items():


            backtester = (
                RiskAdjustedWalkForwardBacktester()
            )


            bets = backtester.run(df)


            filtered = filter_odds(
                bets,
                odds[0],
                odds[1]
            )


            result = calculate_result(
                filtered
            )


            print()

            print(season)

            print(
                f"Bets: {result['bets']}"
            )

            print(
                f"Wins: {result['wins']}"
            )

            print(
                f"Profit: {result['profit']:+.2f}"
            )

            print(
                f"ROI: {result['roi']:+.2f}%"
            )


            total_bets.extend(filtered)



        total = calculate_result(
            total_bets
        )


        print()

        print("TOTAL")

        print(
            f"Bets: {total['bets']}"
        )

        print(
            f"Wins: {total['wins']}"
        )

        print(
            f"Profit: {total['profit']:+.2f}"
        )

        print(
            f"ROI: {total['roi']:+.2f}%"
        )