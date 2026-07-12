import pandas as pd

from src.config.model_config import MODEL_CONFIG
from src.evaluation.platt_calibrator import (
    PlattCalibrator,
)
from src.features.football_features import (
    FootballFeatures,
)
from src.optimization.calibrated_optimizer import (
    CalibratedOptimizer,
)


SEASONS = {

    "2023/24":
        "data/raw/premier_league_2023_24.csv",

    "2024/25":
        "data/raw/premier_league_2024_25.csv",
}



EDGE_RANGES = [

    (0.02, 0.06),

    (0.03, 0.07),

    (0.04, 0.08),

    (0.05, 0.10),

    (0.06, 0.10),

    (0.07, 0.12),

    (0.08, 0.15),

    (0.10, 0.20),

]



def load_season(
    path
):

    df = pd.read_csv(
        path
    )

    return FootballFeatures(
        df
    ).prepare()



def train_calibrator():

    df = pd.read_csv(
        "data/processed/"
        "probability_analysis.csv"
    )


    train = df[
        df["season"]
        ==
        "2022/23"
    ]


    calibrator = PlattCalibrator()


    calibrator.fit(
        train["probability"].tolist(),
        train["actual"].tolist()
    )


    return calibrator



def main():

    print(
        "\n===== CALIBRATED EDGE OPTIMIZER ====="
    )


    MODEL_CONFIG[
        "form_weight"
    ] = 80



    seasons = {

        season:
        load_season(path)

        for season, path
        in SEASONS.items()

    }


    calibrator = train_calibrator()



    optimizer = (
        CalibratedOptimizer(
            calibrator,
            seasons
        )
    )


    results = optimizer.optimize(
        EDGE_RANGES
    )


    print(
        "\n\n===== TOP RESULTS ====="
    )


    for result in results[:5]:

        print(
            "\n--------------------"
        )

        print(
            f"edge: "
            f"{result['min_edge']:.2f}"
            "-"
            f"{result['max_edge']:.2f}"
        )

        print(
            f"Bets: "
            f"{result['total_bets']}"
        )

        print(
            f"Profit: "
            f"{result['total_profit']:+.2f}"
        )

        print(
            f"ROI: "
            f"{result['combined_roi']:+.2f}%"
        )

        print(
            "Profitable seasons: "
            f"{result['profitable_seasons']}/2"
        )



if __name__ == "__main__":

    main()