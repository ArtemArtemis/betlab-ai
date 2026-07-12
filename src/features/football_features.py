import pandas as pd


class FootballFeatures:

    REQUIRED_COLUMNS = [
        "Date",
        "HomeTeam",
        "AwayTeam",
        "FTHG",
        "FTAG",
        "AvgH",
        "AvgD",
        "AvgA",
    ]

    def __init__(self, df):
        self.df = df.copy()

    def prepare(self):

        print("Preparing football features...")

        self._validate_columns()

        self.df["Date"] = pd.to_datetime(
            self.df["Date"],
            dayfirst=True,
            errors="coerce"
        )

        self.df = self.df.dropna(
            subset=[
                "Date",
                "HomeTeam",
                "AwayTeam",
                "FTHG",
                "FTAG",
            ]
        )

        self.df = self.df.sort_values(
            by="Date"
        ).reset_index(
            drop=True
        )

        self.df["Result"] = self.df.apply(
            self._get_result,
            axis=1
        )

        self.df["GoalDifference"] = (
            self.df["FTHG"]
            -
            self.df["FTAG"]
        )

        self.df["HomeOdds"] = pd.to_numeric(
            self.df["AvgH"],
            errors="coerce"
        )

        self.df["DrawOdds"] = pd.to_numeric(
            self.df["AvgD"],
            errors="coerce"
        )

        self.df["AwayOdds"] = pd.to_numeric(
            self.df["AvgA"],
            errors="coerce"
        )

        return self.df

    def _validate_columns(self):

        missing_columns = [
            column
            for column in self.REQUIRED_COLUMNS
            if column not in self.df.columns
        ]

        if missing_columns:
            raise ValueError(
                "Missing required columns: "
                +
                ", ".join(missing_columns)
            )

    def _get_result(self, row):

        if row["FTHG"] > row["FTAG"]:
            return "H"

        if row["FTHG"] < row["FTAG"]:
            return "A"

        return "D"

    def save(self, df):

        output_file = (
            "data/processed/"
            "premier_league_features.csv"
        )

        df.to_csv(
            output_file,
            index=False
        )

        print(
            f"Saved features: {output_file}"
        )