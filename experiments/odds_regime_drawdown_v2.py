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

    "3.0-4.0": 0.10,

    "4.0-5.0": 0.12,

    "5.0+": 0.06

}



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


    if 3.0 <= odds < 4.0:

        return "3.0-4.0"


    if 4.0 <= odds < 5.0:

        return "4.0-5.0"


    if odds >= 5.0:

        return "5.0+"



    return None



def apply_filter(
    bets
):

    selected = []


    for bet in bets:


        regime = get_regime(
            bet["odds"]
        )


        if regime is None:

            continue



        if (
            bet["edge"]
            >=
            FILTERS[regime]
        ):

            selected.append(
                bet
            )



    return selected



def drawdown_report(
    bets
):


    bankroll = 1000

    peak = bankroll

    max_drawdown = 0

    max_drawdown_percent = 0


    loss_streak = 0

    max_loss_streak = 0


    win_streak = 0

    max_win_streak = 0



    for bet in bets:


        bankroll += (
            bet["profit"]
        )


        if bankroll > peak:

            peak = bankroll



        drawdown = (
            peak
            -
            bankroll
        )


        percent = (

            drawdown
            /
            peak
            *
            100

        )


        if percent > max_drawdown_percent:

            max_drawdown_percent = percent

            max_drawdown = drawdown



        if bet["win"]:

            win_streak += 1

            loss_streak = 0


        else:

            loss_streak += 1

            win_streak = 0



        max_loss_streak = max(
            max_loss_streak,
            loss_streak
        )


        max_win_streak = max(
            max_win_streak,
            win_streak
        )



    return {

        "bets":
            len(bets),

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
            max_win_streak

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


        filtered = apply_filter(
            bets
        )


        all_bets.extend(
            filtered
        )



    print()

    print("==============================")

    print(
        "ODDS REGIME DRAWDOWN ANALYSIS"
    )

    print("==============================")


    print(
        drawdown_report(
            all_bets
        )
    )



if __name__ == "__main__":
    run()