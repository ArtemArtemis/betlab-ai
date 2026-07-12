import pandas as pd

from src.features.football_features import FootballFeatures
from src.optimization.optimizer import ParameterOptimizer


def main():

    df = pd.read_csv(
        "data/raw/premier_league.csv"
    )


    features = FootballFeatures(
        df
    )

    df = features.prepare()


    optimizer = ParameterOptimizer(
        df
    )


    optimizer.run(
        form_weights=[
            40,
            60,
            80,
            100,
            120
        ],
        edge_ranges=[
            (0.05, 0.10),
            (0.06, 0.10),
            (0.07, 0.10),
            (0.07, 0.12),
            (0.08, 0.12)
        ]
    )


    optimizer.report()


if __name__ == "__main__":

    main()