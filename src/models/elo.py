import math


class EloRating:

    def __init__(
        self,
        initial_rating=1500,
        k_factor=20,
        home_advantage=60
    ):

        self.ratings = {}

        self.initial_rating = initial_rating
        self.k_factor = k_factor
        self.home_advantage = home_advantage


    def get_rating(self, team):

        if team not in self.ratings:
            self.ratings[team] = self.initial_rating

        return self.ratings[team]


    def expected_score(
        self,
        home_rating,
        away_rating
    ):

        return 1 / (
            1 +
            10 ** (
                (
                    away_rating
                    -
                    (home_rating + self.home_advantage)
                )
                /
                400
            )
        )


    def update(
        self,
        home_team,
        away_team,
        result,
        goal_difference
    ):

        home_rating = self.get_rating(home_team)
        away_rating = self.get_rating(away_team)


        expected = self.expected_score(
            home_rating,
            away_rating
        )


        if result == "H":
            actual = 1

        elif result == "A":
            actual = 0

        else:
            actual = 0.5


        # сила победы/поражения
        margin = math.log(
            abs(goal_difference) + 1
        )


    
        change = (
            self.k_factor
            *
            margin
            *
            (actual - expected)
        )


        self.ratings[home_team] = round(
            home_rating + change
        )

        self.ratings[away_team] = round(
            away_rating - change
        )