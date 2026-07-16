class DynamicThreeWayProbability:


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


        diff = (
            home_rating
            -
            away_rating
        )


        adjusted_diff = (
            diff
            +
            self.home_advantage
        )


        home_strength = (
            1 /
            (
                1 +
                10 ** (
                    -adjusted_diff / 400
                )
            )
        )


        away_strength = (
            1 -
            home_strength
        )


        # Dynamic draw probability

        abs_diff = abs(diff)


        if abs_diff < 50:

            draw_probability = 0.32


        elif abs_diff < 150:

            draw_probability = 0.25


        else:

            draw_probability = 0.18



        remaining = (
            1 -
            draw_probability
        )


        home_probability = (
            home_strength
            *
            remaining
        )


        away_probability = (
            away_strength
            *
            remaining
        )


        return {

            "home_win":
                round(home_probability,3),

            "draw":
                round(draw_probability,3),

            "away_win":
                round(away_probability,3)

        }