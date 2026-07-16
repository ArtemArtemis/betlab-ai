from src.backtesting.dynamic_stake_walk_forward import (
    DynamicStakeWalkForwardBacktester
)

from src.betting.dynamic_stake_optimizer import (
    DynamicStakeOptimizer
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



def load(path):

    df = pd.read_csv(path)

    return FootballFeatures(df).prepare()



datasets = {

    season:
    load(path)

    for season, path in SEASONS.items()

}



print(
    "\n=============================="
)

print(
    "DYNAMIC STAKE OPTIMIZATION"
)

print(
    "=============================="
)



for variant in [
    "A",
    "B",
    "C"
]:

    print(
        f"\nVariant {variant}: "
        f"{DynamicStakeOptimizer.VARIANTS[variant]['name']}"
    )


    total_profit = 0

    total_bets = 0


    for season, df in datasets.items():


        backtester = (
            DynamicStakeWalkForwardBacktester()
        )


        backtester.dynamic_stake = (
            DynamicStakeOptimizer(
                variant=variant
            )
        )


        bets = backtester.run(df)


        profit = sum(
            bet["profit"]
            for bet in bets
        )


        total_profit += profit

        total_bets += len(bets)



    roi = (
        total_profit
        /
        (total_bets * 10)
    )


    print(
        f"Bets: {total_bets}"
    )

    print(
        f"Profit: {total_profit:+.2f}"
    )

    print(
        f"ROI: {roi:+.2%}"
    )