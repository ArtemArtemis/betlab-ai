class ConditionalHomeAwayFilter:


    def __init__(
        self,
        odds_threshold=3.0,
        min_form=0.5
    ):

        self.odds_threshold = odds_threshold
        self.min_form = min_form



    def needs_filter(
        self,
        odds
    ):

        return (
            odds >= self.odds_threshold
        )



    def allow_bet(
        self,
        odds,
        form
    ):

        if not self.needs_filter(odds):

            return True


        return (
            form >= self.min_form
        )