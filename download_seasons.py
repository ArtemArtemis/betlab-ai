from pathlib import Path

import pandas as pd


SEASONS = {
    "2023_24": (
        "https://www.football-data.co.uk/"
        "mmz4281/2324/E0.csv"
    ),
    "2024_25": (
        "https://www.football-data.co.uk/"
        "mmz4281/2425/E0.csv"
    )
}


def download_seasons():

    output_directory = Path(
        "data/raw"
    )

    output_directory.mkdir(
        parents=True,
        exist_ok=True
    )


    for season, url in SEASONS.items():

        output_file = (
            output_directory
            /
            f"premier_league_{season}.csv"
        )


        print(
            f"Downloading season {season}..."
        )


        try:

            df = pd.read_csv(
                url
            )

        except Exception as error:

            print(
                f"Failed to download {season}: "
                f"{error}"
            )

            continue


        required_columns = {
            "Date",
            "HomeTeam",
            "AwayTeam",
            "FTHG",
            "FTAG",
            "AvgH",
            "AvgD",
            "AvgA"
        }


        missing_columns = (
            required_columns
            -
            set(df.columns)
        )


        if missing_columns:

            print(
                f"Season {season} is missing columns: "
                f"{sorted(missing_columns)}"
            )

            continue


        df.to_csv(
            output_file,
            index=False
        )


        print(
            f"Saved {len(df)} matches to "
            f"{output_file}"
        )


if __name__ == "__main__":

    download_seasons()