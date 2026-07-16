import pandas as pd


from src.features.football_features import FootballFeatures

from src.backtesting.risk_adjusted_walk_forward import (
    RiskAdjustedWalkForwardBacktester
)



TEST_FILTERS = {

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



def calculate_report(
    bets
):

    profit = sum(
        b["profit"]
        for b in bets
    )


    wins = sum(
        1
        for b in bets
        if b["win"]
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
            TEST_FILTERS[regime]
        ):

            selected.append(
                bet
            )


    return selected



def run_test(
    train,
    test
):


    print()
    print("==============================")
    print(
        "TRAIN:",
        train
    )

    print(
        "TEST:",
        test
    )



    # train загрузка нужна только для соблюдения walk-forward структуры

    for season in train:

        load_season(
            season
        )



    df_test = load_season(
        test
    )


    backtester = (
        RiskAdjustedWalkForwardBacktester()
    )


    bets = backtester.run(
        df_test
    )


    filtered = apply_filter(
        bets
    )


    result = calculate_report(
        filtered
    )


    result["test"] = test


    print(
        result
    )



def run():


    run_test(

        [
            "2022_23"
        ],

        "2023_24"

    )


    run_test(

        [
            "2022_23",
            "2023_24"
        ],

        "2024_25"

    )



if __name__ == "__main__":
    run()