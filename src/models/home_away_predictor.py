from src.config.model_config import MODEL_CONFIG


class HomeAwayPredictor:


    def __init__(self):

        self.home_advantage = MODEL_CONFIG[
            "home_advantage"
        ]

        self.form_weight = MODEL_CONFIG[
            "form_weight"
        ]


    def predict(
        self,
        home_rating,
        away_rating,
        home_away_form_difference=0
    ):


        adjusted_home_rating = (
            home_rating
            +
            self.home_advantage
            +
            (
                home_away_form_difference
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