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


ODDS_MIN = 3.0
ODDS_MAX = 6.0



def load_features(path):

    df = pd.read_csv(path)

    features = FootballFeatures(df)

    return features.prepare()



def filter_odds(bets):

    return [

        bet

        for bet in bets

        if ODDS_MIN <= bet["odds"] <= ODDS_MAX

    ]



def calculate_report(bets):


    if len(bets) == 0:

        return {

            "bets": 0,

            "profit": 0,

            "roi": 0

        }



    profit = sum(

        b["profit"]

        for b in bets

    )


    stake = sum(

        b["stake"]

        for b in bets

    )


    roi = (

        profit / stake * 100

        if stake > 0

        else 0

    )


    wins = sum(

        1

        for b in bets

        if b["win"]

    )


    return {

        "bets": len(bets),

        "wins": wins,

        "profit": round(profit,2),

        "roi": round(roi,2)

    }



if __name__ == "__main__":


    print()

    print("==============================")

    print("ODDS REGIME SEASON TEST")

    print("==============================")



    total_bets = []



    for season, path in SEASONS.items():


        print()

        print("==============================")

        print(season)

        print("==============================")


        df = load_features(path)



        backtester = (

            RiskAdjustedWalkForwardBacktester()

        )


        bets = backtester.run(df)


        filtered = filter_odds(bets)



        result = calculate_report(filtered)



        total_bets.extend(filtered)



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



    print()

    print("==============================")

    print("TOTAL 3.0-6.0 ODDS")

    print("==============================")


    result = calculate_report(
        total_bets
    )


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