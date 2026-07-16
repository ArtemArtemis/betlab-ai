from src.features.football_features import FootballFeatures

from src.backtesting.risk_adjusted_walk_forward import (
    RiskAdjustedWalkForwardBacktester
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



def calculate_drawdown(
    bets
):


    bankroll = 1000

    peak = bankroll

    max_drawdown = 0

    max_drawdown_percent = 0

    current_loss_streak = 0

    max_loss_streak = 0

    current_win_streak = 0

    max_win_streak = 0



    history = []



    for bet in bets:


        bankroll += (
            bet["profit"]
        )


        history.append(
            bankroll
        )


        if bankroll > peak:

            peak = bankroll



        drawdown = (
            peak
            -
            bankroll
        )


        drawdown_percent = (

            drawdown
            /
            peak
            *
            100

        )


        if drawdown_percent > max_drawdown_percent:

            max_drawdown_percent = (
                drawdown_percent
            )

            max_drawdown = drawdown



        if bet["win"]:

            current_win_streak += 1

            current_loss_streak = 0


        else:

            current_loss_streak += 1

            current_win_streak = 0



        max_loss_streak = max(
            max_loss_streak,
            current_loss_streak
        )


        max_win_streak = max(
            max_win_streak,
            current_win_streak
        )



    return {

        "final_bankroll":
            round(
                bankroll,
                2
            ),

        "profit":
            round(
                bankroll - 1000,
                2
            ),

        "max_drawdown":
            round(
                max_drawdown,
                2
            ),

        "max_drawdown_percent":
            round(
                max_drawdown_percent,
                2
            ),

        "max_loss_streak":
            max_loss_streak,

        "max_win_streak":
            max_win_streak,

        "bets":
            len(bets)

    }



def run():


    all_bets = []



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


        all_bets.extend(
            bets
        )



    print()
    print("==============================")
    print("TEAM STRENGTH DRAWDOWN ANALYSIS")
    print("==============================")


    result = calculate_drawdown(
        all_bets
    )


    print(
        result
    )



if __name__ == "__main__":
    run()