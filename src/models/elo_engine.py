from src.models.elo import EloRating


class EloEngine:

    def __init__(self):

        self.elo = EloRating()


    def process_matches(self, df):

        print("Running Elo Engine...")


        for _, match in df.iterrows():

            home = match["HomeTeam"]
            away = match["AwayTeam"]

            result = match["Result"]

            goal_difference = match["GoalDifference"]


            self.elo.update(
                home,
                away,
                result,
                goal_difference
            )


        return self.elo.ratings



    def print_ratings(self):

        print("\n===== FINAL ELO =====")


        ratings = sorted(
            self.elo.ratings.items(),
            key=lambda x: x[1],
            reverse=True
        )


        for team, rating in ratings:

            print(
                f"{team:20} {rating}"
            )



    def save_ratings(self):

        import pandas as pd

        df = pd.DataFrame(
            list(self.elo.ratings.items()),
            columns=[
                "Team",
                "Elo"
            ]
        )

        df = df.sort_values(
            by="Elo",
            ascending=False
        )

        df.to_csv(
            "data/processed/elo_ratings.csv",
            index=False
        )

        print(
            "Saved Elo ratings"
        )