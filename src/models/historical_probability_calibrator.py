class HistoricalProbabilityCalibrator:


    def __init__(self):

        self.buckets = {}



    def fit(
        self,
        predictions,
        outcomes,
        bins=10
    ):

        self.buckets = {}


        for i in range(bins):

            low = i / bins

            high = (i + 1) / bins


            results = []


            for prediction, outcome in zip(
                predictions,
                outcomes
            ):

                if (
                    prediction >= low
                    and prediction < high
                ):

                    results.append(
                        outcome
                    )


            if results:

                self.buckets[
                    (
                        round(low, 2),
                        round(high, 2)
                    )
                ] = sum(results) / len(results)



        return self



    def calibrate(
        self,
        probability
    ):


        for (
            low,
            high
        ), value in self.buckets.items():


            if (
                probability >= low
                and probability < high
            ):

                return round(
                    value,
                    3
                )


        return probability