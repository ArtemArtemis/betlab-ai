from collections import defaultdict, deque

from src.config.model_config import MODEL_CONFIG



class HomeAwayForm:


    def __init__(self):

        self.window = MODEL_CONFIG[
            "form_window"
        ]


        self.home_history = defaultdict(
            lambda: deque(
                maxlen=self.window
            )
        )


        self.away_history = defaultdict(
            lambda: deque(
                maxlen=self.window
            )
        )



    def get_score(
        self,
        history
    ):

        if len(history) == 0:

            return 0.5


        points = sum(history)

        maximum = len(history) * 3


        return points / maximum



    def get_home_score(
        self,
        team
    ):

        return self.get_score(
            self.home_history[team]
        )



    def get_away_score(
        self,
        team
    ):

        return self.get_score(
            self.away_history[team]
        )



    def get_difference(
        self,
        home_team,
        away_team
    ):

        home_strength = (
            self.get_home_score(
                home_team
            )
        )


        away_strength = (
            self.get_away_score(
                away_team
            )
        )


        return (
            home_strength
            -
            away_strength
        )



    def update(
        self,
        home_team,
        away_team,
        result
    ):

        if result == "H":

            self.home_history[
                home_team
            ].append(3)

            self.away_history[
                away_team
            ].append(0)


        elif result == "A":

            self.home_history[
                home_team
            ].append(0)

            self.away_history[
                away_team
            ].append(3)


        else:

            self.home_history[
                home_team
            ].append(1)

            self.away_history[
                away_team
            ].append(1)