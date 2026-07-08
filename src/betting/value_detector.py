class ValueDetector:


    def calculate_implied_probability(
        self,
        odds
    ):

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
        edge,
        threshold=0.05
    ):

        return edge >= threshold