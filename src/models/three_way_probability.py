class ThreeWayProbability:


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


        rating_difference = (
            home_rating
            -
            away_rating
            +
            self.home_advantage
        )


        home_strength = (
            1 /
            (
                1 +
                10 ** (
                    -rating_difference / 400
                )
            )
        )


        away_strength = (
            1 -
            home_strength
        )


        # draw probability
        # base football assumption

        draw_probability = (
            0.25
        )


        home_probability = (
            home_strength
            *
            (
                1 - draw_probability
            )
        )


        away_probability = (
            away_strength
            *
            (
                1 - draw_probability
            )
        )


        return {

            "home_win":
                round(
                    home_probability,
                    3
                ),

            "draw":
                round(
                    draw_probability,
                    3
                ),

            "away_win":
                round(
                    away_probability,
                    3
                )

        }