from src.backtesting.risk_adjusted_walk_forward import (
    RiskAdjustedWalkForwardBacktester
)

from src.features.football_features import FootballFeatures

import pandas as pd

from src.config.model_config import MODEL_CONFIG



SEASONS = {

    "2022/23":
        "data/raw/premier_league_2022_23.csv",

    "2023/24":
        "data/raw/premier_league_2023_24.csv",

    "2024/25":
        "data/raw/premier_league_2024_25.csv"

}



EDGE_VARIANTS = {

    "5_percent": 0.05,

    "7_percent_CONTROL": 0.07,

    "8_percent": 0.08,

    "10_percent": 0.10,

    "12_percent": 0.12

}



def load_seasons():

    datasets = {}

    for season, path in SEASONS.items():

        df = pd.read_csv(path)

        datasets[season] = (
            FootballFeatures(df).prepare()
        )

    return datasets



class EdgeRiskWrapper:


    def __init__(
        self,
        min_edge
    ):

        self.min_edge = min_edge



    def run(
        self,
        df
    ):

        backtester = (
            RiskAdjustedWalkForwardBacktester()
        )


        backtester.value_detector.min_edge = (
            self.min_edge
        )


        return backtester.run(df)



def calculate_result(
    bets
):

    profit = sum(
        bet["profit"]
        for bet in bets
    )


    stake = sum(
        bet["stake"]
        for bet in bets
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



if __name__ == "__main__":


    datasets = load_seasons()


    print(
        "\n=============================="
    )

    print(
        "RISK EDGE OPTIMIZATION"
    )

    print(
        "=============================="
    )



    for name, edge in EDGE_VARIANTS.items():


        total_bets = []



        for season, df in datasets.items():


            model = EdgeRiskWrapper(
                edge
            )


            bets = model.run(df)


            total_bets.extend(
                bets
            )



        result = calculate_result(
            total_bets
        )



        print(
            f"\n{name}"
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