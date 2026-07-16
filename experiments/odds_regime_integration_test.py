from src.features.football_features import FootballFeatures

from src.backtesting.risk_adjusted_walk_forward import (
    RiskAdjustedWalkForwardBacktester
)

from src.betting.odds_regime_filter import (
    OddsRegimeFilter
)

import pandas as pd



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



def run_filter(
    bets
):


    filter_model = (
        OddsRegimeFilter()
    )


    selected = []


    for bet in bets:


        if filter_model.is_valid(
            bet["odds"],
            bet["edge"]
        ):

            selected.append(
                bet
            )


    return selected



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


        filtered = run_filter(
            bets
        )


        all_bets.extend(
            filtered
        )



    print()

    print("==============================")

    print(
        "ODDS REGIME INTEGRATION TEST"
    )

    print("==============================")


    print(
        calculate_report(
            all_bets
        )
    )



if __name__ == "__main__":
    run()