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



ODDS_VARIANTS = {

    "CONTROL_NO_FILTER":
        (0, 100),

    "1.5_3.0":
        (1.5, 3.0),

    "2.0_4.0":
        (2.0, 4.0),

    "3.0_6.0":
        (3.0, 6.0),

    "4_PLUS":
        (4.0, 100)

}



class OddsFilteredBacktester:


    def __init__(
        self,
        min_odds,
        max_odds
    ):

        self.min_odds = min_odds

        self.max_odds = max_odds



    def run(
        self,
        df
    ):


        backtester = (
            RiskAdjustedWalkForwardBacktester()
        )


        bets = backtester.run(df)



        filtered = []


        for bet in bets:


            if (

                bet["odds"] >= self.min_odds

                and

                bet["odds"] <= self.max_odds

            ):

                filtered.append(
                    bet
                )


        return filtered



def calculate_result(
    bets
):


    if not bets:

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

        profit / stake

        if stake

        else 0

    )


    return {

        "bets":
            len(bets),

        "profit":
            round(
                profit,
                2
            ),

        "roi":
            round(
                roi * 100,
                2
            )

    }



def load_data():


    datasets = {}


    for season, path in SEASONS.items():

        df = pd.read_csv(path)

        datasets[season] = (
            FootballFeatures(df).prepare()
        )


    return datasets




if __name__ == "__main__":


    datasets = load_data()



    print()

    print(
        "=============================="
    )

    print(
        "ODDS REGIME OPTIMIZATION"
    )

    print(
        "=============================="
    )



    for name, odds_range in ODDS_VARIANTS.items():


        all_bets = []


        for season, df in datasets.items():


            model = OddsFilteredBacktester(

                odds_range[0],

                odds_range[1]

            )


            bets = model.run(df)


            all_bets.extend(
                bets
            )



        result = calculate_result(
            all_bets
        )



        print()

        print(
            name
        )

        print(
            f"Bets: {result['bets']}"
        )

        print(
            f"Profit: {result['profit']:+.2f}"
        )

        print(
            f"ROI: {result['roi']:+.2f}%"
        )