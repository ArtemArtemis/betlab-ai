class ProbabilityCalibration:


    def __init__(self):

        self.calibration_map = {

            "1.5-2.5": 0.85,

            "2.5-3.5": 0.72,

            "3.5-5.0": 0.54,

            "5.0+": 0.39

        }



    def get_odds_bucket(
        self,
        odds
    ):


        if odds < 2.5:

            return "1.5-2.5"


        elif odds < 3.5:

            return "2.5-3.5"


        elif odds < 5.0:

            return "3.5-5.0"


        else:

            return "5.0+"




    def calibrate(
        self,
        probability,
        odds
    ):


        bucket = (
            self.get_odds_bucket(
                odds
            )
        )


        factor = (
            self.calibration_map[
                bucket
            ]
        )


        calibrated_probability = (

            probability
            *
            factor

        )


        return {

            "raw_probability":
                probability,

            "calibrated_probability":
                round(
                    calibrated_probability,
                    4
                ),

            "bucket":
                bucket,

            "factor":
                factor

        }