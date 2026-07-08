class EloPredictor:

    def __init__(
        self,
        home_advantage=60
    ):
        self.home_advantage = home_advantage


    def predict(
        self,
        home_rating,
        away_rating
    ):

        home_probability = 1 / (
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


        away_probability = 1 - home_probability


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