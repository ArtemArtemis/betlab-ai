import pandas as pd
import requests
from io import BytesIO

from src.config.settings import RAW_DATA_DIR


class FootballDataCollector:

    BASE_URL = "https://www.football-data.co.uk/mmz4281/"

    def __init__(self):
        self.output_file = RAW_DATA_DIR / "premier_league.csv"

    def download_season(self, season):

        url = f"{self.BASE_URL}{season}/E0.csv"

        print(f"Downloading: {url}")

        response = requests.get(url)

        if response.status_code != 200:
            raise Exception(
                f"Download failed: {response.status_code}"
            )

        df = pd.read_csv(
            BytesIO(response.content),
            encoding="utf-8-sig"
        )

        return df

    def save_data(self, df):

        df.to_csv(
            self.output_file,
            index=False
        )

        print(f"Saved: {self.output_file}")