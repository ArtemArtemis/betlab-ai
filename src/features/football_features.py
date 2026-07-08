import pandas as pd


class FootballFeatures:

    def __init__(self, df):
        self.df = df.copy()


    def prepare(self):

        print("Preparing football features...")

        self.df["Date"] = pd.to_datetime(
            self.df["Date"],
            dayfirst=True,
            errors="coerce"
        )

        self.df = self.df.sort_values(
            by="Date"
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


        self.df["HomeOdds"] = self.df["AvgH"]

        self.df["AwayOdds"] = self.df["AvgA"]


        return self.df


    def _get_result(self, row):

        if row["FTHG"] > row["FTAG"]:
            return "H"

        elif row["FTHG"] < row["FTAG"]:
            return "A"

        else:
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