import pandas as pd

from src.features.football_features import FootballFeatures


def main():

    file_path = (
        "data/raw/"
        "premier_league_2024_25.csv"
    )

    raw_dataframe = pd.read_csv(
        file_path
    )

    prepared_dataframe = FootballFeatures(
        raw_dataframe
    ).prepare()

    columns_to_show = [
        "Date",
        "HomeTeam",
        "AwayTeam",
        "HomeOdds",
        "DrawOdds",
        "AwayOdds",
    ]

    print(
        "\n===== ODDS CHECK ====="
    )

    print(
        prepared_dataframe[
            columns_to_show
        ].head(10).to_string(
            index=False
        )
    )

    print(
        "\n===== MISSING ODDS ====="
    )

    print(
        prepared_dataframe[
            [
                "HomeOdds",
                "DrawOdds",
                "AwayOdds",
            ]
        ].isna().sum()
    )


if __name__ == "__main__":
    main()