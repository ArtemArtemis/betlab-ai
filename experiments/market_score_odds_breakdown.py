from collections import defaultdict

import pandas as pd

from src.backtesting.risk_adjusted_walk_forward import (
    RiskAdjustedWalkForwardBacktester
)

from src.features.football_features import FootballFeatures


SEASONS = [
    "2022_23",
    "2023_24",
    "2024_25"
]


def load_season(season):

    path = f"data/raw/premier_league_{season}.csv"

    print(f"Loading {path}")

    df = pd.read_csv(
        path,
        encoding="utf-8"
    )

    features = FootballFeatures(
        df
    )

    df = features.prepare()

    return df



def get_odds_bucket(odds):

    if odds < 3.0:
        return "<3.0"

    elif odds < 4.0:
        return "3.0-4.0"

    elif odds < 5.0:
        return "4.0-5.0"

    else:
        return "5.0+"



def run():

    buckets = defaultdict(
        lambda: {
            "bets": 0,
            "wins": 0,
            "profit": 0
        }
    )


    for season in SEASONS:

        print("="*30)
        print(season)


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


            score = bet.get(
                "market_score",
                None
            )


            if score is None:
                continue


            odds_bucket = get_odds_bucket(
                bet["odds"]
            )


            key = (
                score,
                odds_bucket
            )


            buckets[key]["bets"] += 1


            if bet["win"]:
                buckets[key]["wins"] += 1


            buckets[key]["profit"] += (
                bet["profit"]
            )



    print("\n")
    print("==============================")
    print("MARKET SCORE ODDS BREAKDOWN")
    print("==============================")


    for key,data in sorted(
        buckets.items(),
        reverse=True
    ):

        score, odds_bucket = key


        roi = (
            data["profit"] /
            (data["bets"] * 10)
            * 100
        )


        print(
            {
                "score": score,
                "odds_range": odds_bucket,
                "bets": data["bets"],
                "wins": data["wins"],
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



if __name__ == "__main__":
    run()