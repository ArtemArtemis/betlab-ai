class DrawRiskDetector:


    def __init__(
        self,
        elo_threshold=50,
        form_threshold=0.1
    ):

        self.elo_threshold = elo_threshold
        self.form_threshold = form_threshold



    def high_risk(
        self,
        home_elo,
        away_elo,
        form_difference
    ):

        elo_close = (
            abs(home_elo - away_elo)
            <
            self.elo_threshold
        )


        form_close = (
            abs(form_difference)
            <
            self.form_threshold
        )


        return (
            elo_close
            and
            form_close
        )