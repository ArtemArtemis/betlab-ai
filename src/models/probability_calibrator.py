class ProbabilityCalibrator:


    def __init__(
        self,
        model_weight=0.7,
        market_weight=0.3
    ):

        self.model_weight = model_weight
        self.market_weight = market_weight



    def calibrate(
        self,
        model_probability,
        odds
    ):

        market_probability = 1 / odds


        calibrated = (
            self.model_weight * model_probability
            +
            self.market_weight * market_probability
        )


        return round(
            calibrated,
            3
        )