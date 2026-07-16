class EloFormBlender:


    def __init__(
        self,
        form_weight=0.2
    ):

        self.form_weight = form_weight



    def blend(
        self,
        elo_probability,
        form_difference
    ):

        form_probability = (
            0.5
            +
            (form_difference * 0.05)
        )


        if form_probability < 0:
            form_probability = 0


        if form_probability > 1:
            form_probability = 1



        blended_probability = (

            elo_probability
            *
            (1 - self.form_weight)

            +

            form_probability
            *
            self.form_weight

        )


        return round(
            blended_probability,
            3
        )