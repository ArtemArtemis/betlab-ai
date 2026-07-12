class HomeAwayFilter:


    def __init__(
        self,
        min_form=0
    ):

        self.min_form = min_form



    def allow_home_bet(
        self,
        home_strength
    ):

        return (
            home_strength
            >=
            self.min_form
        )



    def allow_away_bet(
        self,
        away_strength
    ):

        return (
            away_strength
            >=
            self.min_form
        )