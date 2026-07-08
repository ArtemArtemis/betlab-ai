import pandas as pd

from src.config.settings import RAW_DATA_DIR


class FootballDataCollector:
    def __init__(self):
        self.output_file = RAW_DATA_DIR / "sample_matches.csv"

    def create_sample_dataset(self):
        data = {
            "home_team": [
                "Manchester City",
                "Arsenal",
                "Liverpool",
            ],
            "away_team": [
                "Chelsea",
                "Tottenham",
                "Newcastle",
            ],
            "home_goals": [2, 1, 3],
            "away_goals": [1, 1, 0],
        }

        df = pd.DataFrame(data)

        df.to_csv(self.output_file, index=False)

        return df