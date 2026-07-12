from collections import defaultdict
from collections import deque

from src.config.model_config import MODEL_CONFIG


class TeamForm:

    def __init__(self):

        self.window = MODEL_CONFIG[
            "form_window"
        ]

        self.history = defaultdict(
            lambda: deque(
                maxlen=self.window
            )
        )


    def get_score(
        self,
        team
    ):

        matches = self.history[team]


        if len(matches) == 0:

            return 0.5


        earned_points = sum(
            matches
        )

        maximum_points = (
            len(matches)
            *
            3
        )


        return (
            earned_points
            /
            maximum_points
        )


    def get_difference(
        self,
        home_team,
        away_team
    ):

        home_form = self.get_score(
            home_team
        )

        away_form = self.get_score(
            away_team
        )


        return (
            home_form
            -
            away_form
        )


    def update(
        self,
        home_team,
        away_team,
        result
    ):

        if result == "H":

            home_points = 3
            away_points = 0

        elif result == "A":

            home_points = 0
            away_points = 3

        else:

            home_points = 1
            away_points = 1


        self.history[
            home_team
        ].append(
            home_points
        )


        self.history[
            away_team
        ].append(
            away_points
        )