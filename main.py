import pandas as pd

from src.features.football_features import FootballFeatures


def main():

    df = pd.read_csv(
        "data/raw/premier_league.csv"
    )

    features = FootballFeatures(df)

    prepared_df = features.prepare()

    features.save(prepared_df)

    print(
        prepared_df[
            [
                "Date",
                "HomeTeam",
                "AwayTeam",
                "Result"
            ]
        ].head()
    )


if __name__ == "__main__":
    main()