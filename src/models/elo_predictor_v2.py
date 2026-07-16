class EloPredictorV2:


    def predict(
        self,
        home_rating,
        away_rating,
        strength_feature
    ):


        difference = (
            home_rating
            -
            away_rating
            +
            strength_feature
        )


        home_probability = (
            1 /
            (
                1 +
                10 ** (
                    -difference / 400
                )
            )
        )


        away_probability = (
            1 -
            home_probability
        )


        return {

            "home_win":
                round(home_probability, 3),

            "away_win":
                round(away_probability, 3)

        }