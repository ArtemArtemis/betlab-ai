import pandas as pd

from src.features.football_features import FootballFeatures
from src.optimization.multi_season_optimizer import (
    MultiSeasonOptimizer,
)


def load_season(file_path):
    """
    Загружает исходный CSV и применяет
    существующий FootballFeatures.
    """

    raw_dataframe = pd.read_csv(file_path)

    features = FootballFeatures(raw_dataframe)

    prepared_dataframe = features.prepare()

    return prepared_dataframe


def main():
    print(
        "Loading Premier League seasons..."
    )

    season_2023_24 = load_season(
        "data/raw/premier_league_2023_24.csv"
    )

    season_2024_25 = load_season(
        "data/raw/premier_league_2024_25.csv"
    )

    seasons = {
        "2023/24": season_2023_24,
        "2024/25": season_2024_25,
    }

    optimizer = MultiSeasonOptimizer(
        seasons=seasons
    )

    optimizer.run(
        form_weights=[
            40,
            60,
            80,
            100,
            120,
        ],
        edge_ranges=[
            (0.05, 0.10),
            (0.06, 0.10),
            (0.07, 0.10),
            (0.07, 0.12),
            (0.08, 0.12),
        ],
    )

    optimizer.report(
        top_n=10
    )


if __name__ == "__main__":
    main()