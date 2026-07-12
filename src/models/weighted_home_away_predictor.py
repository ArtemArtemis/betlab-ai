from src.config.model_config import MODEL_CONFIG



class WeightedHomeAwayPredictor:


    def __init__(self):

        self.home_advantage = MODEL_CONFIG[
            "home_advantage"
        ]



    def predict(
        self,
        home_rating,
        away_rating,
        weighted_form_difference=0
    ):


        adjusted_home_rating = (

            home_rating

            +

            self.home_advantage

            +

            (
                weighted_form_difference
                *
                80
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

            "home_win":
                round(
                    home_probability,
                    3
                ),

            "away_win":
                round(
                    away_probability,
                    3
                )

        }