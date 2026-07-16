class ConfidenceCalibrator:


    def __init__(
        self,
        confidence=0.7
    ):

        self.confidence = confidence



    def calibrate(
        self,
        probability
    ):

        calibrated = (
            0.5
            +
            self.confidence
            *
            (
                probability
                -
                0.5
            )
        )

        return round(
            calibrated,
            3
        )