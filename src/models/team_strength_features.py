class TeamStrengthFeatures:


    def __init__(self):

        self.home_advantage_weight = 0.3



    def calculate(
        self,
        elo_difference,
        form_difference
    ):

        strength = (
            elo_difference
            +
            form_difference * 100
        )


        return round(
            strength,
            3
        )