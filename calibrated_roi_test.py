from copy import deepcopy

import pandas as pd

from src.config.model_config import MODEL_CONFIG
from src.features.football_features import FootballFeatures
from src.evaluation.platt_calibrator import PlattCalibrator
from src.backtesting.calibrated_walk_forward import (
    CalibratedWalkForwardBacktester,
)


SEASONS = {
    "2022/23":
        "data/raw/premier_league_2022_23.csv",

    "2023/24":
        "data/raw/premier_league_2023_24.csv",

    "2024/25":
        "data/raw/premier_league_2024_25.csv",
}


CONTROL_PARAMETERS = {
    "form_weight": 80,
    "min_edge": 0.07,
    "max_edge": 0.12,
}


def load_season(path):

    df = pd.read_csv(
        path
    )

    return FootballFeatures(
        df
    ).prepare()


def load_calibration_data():

    df = pd.read_csv(
        "data/processed/"
        "probability_analysis.csv"
    )

    return df



def train_calibrator(
    seasons
):

    train = seasons[
        seasons["season"].isin(
            [
                "2022/23"
            ]
        )
    ]

    calibrator = PlattCalibrator()

    calibrator.fit(
        train["probability"].tolist(),
        train["actual"].tolist()
    )

    return calibrator



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
        profit / stake * 100
        if stake
        else 0
    )

    return {
        "bets": len(bets),
        "profit": profit,
        "roi": roi
    }



def main():

    print(
        "\n===== CALIBRATED ROI TEST ====="
    )


    calibration_data = (
        load_calibration_data()
    )


    original_config = deepcopy(
        MODEL_CONFIG
    )


    try:

        MODEL_CONFIG["form_weight"] = (
            CONTROL_PARAMETERS["form_weight"]
        )

        MODEL_CONFIG["min_edge"] = (
            CONTROL_PARAMETERS["min_edge"]
        )

        MODEL_CONFIG["max_edge"] = (
            CONTROL_PARAMETERS["max_edge"]
        )


        calibrator = train_calibrator(
            calibration_data
        )


        print(
            "\nCalibration parameters:"
        )

        print(
            calibrator.get_parameters()
        )


        for season_name in [
            "2023/24",
            "2024/25"
        ]:


            print(
                f"\nRunning {season_name}"
            )


            df = load_season(
                SEASONS[season_name]
            )


            backtester = (
                CalibratedWalkForwardBacktester(
                    calibrator
                )
            )


            bets = backtester.run(
                df
            )


            result = calculate_result(
                bets
            )


            print(
                "\nRESULT"
            )

            print(
                result
            )


    finally:

        MODEL_CONFIG.clear()

        MODEL_CONFIG.update(
            original_config
        )



if __name__ == "__main__":

    main()