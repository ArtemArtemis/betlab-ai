import pandas as pd


class DataValidator:

    def __init__(self, df):
        self.df = df


    def report(self):

        print("\n===== DATA REPORT =====")

        print(
            f"Rows: {len(self.df)}"
        )

        print(
            f"Columns: {len(self.df.columns)}"
        )


        print("\nMissing values:")

        missing = self.df.isnull().sum()

        print(
            missing[missing > 0]
        )


        print("\nTeams:")

        print(
            self.df["HomeTeam"]
            .nunique()
        )


        print("\nDate range:")

        print(
            self.df["Date"].iloc[0],
            "-",
            self.df["Date"].iloc[-1]
        )