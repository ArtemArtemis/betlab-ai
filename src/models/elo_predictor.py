class EloPredictor:

    def __init__(
        self,
        home_advantage=60,
        form_weight=80
    ):

        self.home_advantage = home_advantage

        self.form_weight = form_weight


    def predict(
        self,
        home_rating,
        away_rating,
        form_difference=0
    ):

        adjusted_home_rating = (
            home_rating
            +
            self.home_advantage
            +
            (
                form_difference
                *
                self.form_weight
            )
        )


        home_probability = 1 / (
            1
            +
            10 ** (
                (
                    away_rating
                    -
                    adjusted_home_rating
                )
                /
                400
            )
        )


        away_probability = (
            1
            -
            home_probability
        )


        return {
            "home_win": round(
                home_probability,
                3
            ),
            "away_win": round(
                away_probability,
                3
            )
        }