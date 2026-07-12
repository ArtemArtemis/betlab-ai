import math

from src.config.model_config import MODEL_CONFIG


class EloRating:

    def __init__(self):

        self.ratings = {}

        self.initial_rating = MODEL_CONFIG[
            "initial_rating"
        ]

        self.k_factor = MODEL_CONFIG[
            "k_factor"
        ]

        self.home_advantage = MODEL_CONFIG[
            "home_advantage"
        ]


    def get_rating(
        self,
        team
    ):

        if team not in self.ratings:

            self.ratings[team] = (
                self.initial_rating
            )


        return self.ratings[team]


    def expected_score(
        self,
        home_rating,
        away_rating
    ):

        return 1 / (
            1
            +
            10 ** (
                (
                    away_rating
                    -
                    (
                        home_rating
                        +
                        self.home_advantage
                    )
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

        home_rating = self.get_rating(
            home_team
        )

        away_rating = self.get_rating(
            away_team
        )


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


        margin = math.log(
            abs(goal_difference) + 1
        )


        change = (
            self.k_factor
            *
            margin
            *
            (
                actual
                -
                expected
            )
        )


        self.ratings[home_team] = round(
            home_rating + change
        )


        self.ratings[away_team] = round(
            away_rating - change
        )