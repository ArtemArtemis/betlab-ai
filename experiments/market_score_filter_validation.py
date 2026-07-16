import pandas as pd


from src.backtesting.risk_adjusted_walk_forward import (
    RiskAdjustedWalkForwardBacktester
)

from src.features.football_features import FootballFeatures



TRAIN_TESTS = [

    {
        "train": [
            "2022_23"
        ],
        "test": "2023_24"
    },

    {
        "train": [
            "2022_23",
            "2023_24"
        ],
        "test": "2024_25"
    }

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



def prepare_train(
    seasons
):

    frames = []


    for season in seasons:

        frames.append(
            load_season(
                season
            )
        )


    return pd.concat(
        frames,
        ignore_index=True
    )



def calculate_result(
    bets
):

    filtered = []


    for bet in bets:


        if (
            bet.get(
                "market_score"
            )
            == 2
            and
            bet.get(
                "odds",
                0
            )
            >= 5.0
        ):

            filtered.append(
                bet
            )


    profit = sum(
        x["profit"]
        for x in filtered
    )


    wins = sum(
        1
        for x in filtered
        if x["win"]
    )


    bets_count = len(
        filtered
    )


    roi = (
        profit /
        (bets_count * 10)
        * 100
        if bets_count
        else 0
    )


    return {

        "bets": bets_count,

        "wins": wins,

        "win_rate":
            round(
                wins /
                bets_count *
                100,
                2
            )
            if bets_count
            else 0,

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


    results = []


    for block in TRAIN_TESTS:


        print("="*40)

        print(
            "TRAIN:",
            block["train"]
        )

        print(
            "TEST:",
            block["test"]
        )


        train_df = prepare_train(
            block["train"]
        )


        test_df = load_season(
            block["test"]
        )


        combined = pd.concat(
            [
                train_df,
                test_df
            ],
            ignore_index=True
        )


        backtester = (
            RiskAdjustedWalkForwardBacktester()
        )


        bets = backtester.run(
            combined
        )


        result = calculate_result(
            bets
        )


        result["test"] = (
            block["test"]
        )


        print(
            "FILTER RESULT:"
        )

        print(
            result
        )


        results.append(
            result
        )



    print("\n")
    print("==============================")
    print("FINAL MARKET SCORE FILTER OOS")
    print("==============================")


    for r in results:

        print(
            r
        )



if __name__ == "__main__":

    run()