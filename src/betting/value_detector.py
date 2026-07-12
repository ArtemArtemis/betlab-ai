from src.config.model_config import MODEL_CONFIG


class ValueDetector:

    def __init__(self):

        self.min_edge = MODEL_CONFIG[
            "min_edge"
        ]

        self.max_edge = MODEL_CONFIG[
            "max_edge"
        ]


    def calculate_implied_probability(
        self,
        odds
    ):

        if odds is None or odds <= 1:

            return None


        return round(
            1 / odds,
            3
        )


    def calculate_edge(
        self,
        model_probability,
        odds
    ):

        market_probability = (
            self.calculate_implied_probability(
                odds
            )
        )


        if market_probability is None:

            return {
                "model_probability": model_probability,
                "market_probability": None,
                "edge": None
            }


        edge = (
            model_probability
            -
            market_probability
        )


        return {
            "model_probability": model_probability,
            "market_probability": market_probability,
            "edge": round(edge, 3)
        }


    def is_value_bet(
        self,
        edge
    ):

        if edge is None:

            return False


        return (
            self.min_edge
            <= edge
            <= self.max_edge
        )