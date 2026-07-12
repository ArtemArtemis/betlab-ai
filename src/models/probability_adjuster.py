class ProbabilityAdjuster:


    def __init__(
        self,
        draw_penalty=0.05
    ):

        self.draw_penalty = draw_penalty



    def adjust(
        self,
        probability,
        draw_risk
    ):


        if draw_risk:

            probability -= self.draw_penalty


        if probability < 0:

            probability = 0


        if probability > 1:

            probability = 1


        return probability