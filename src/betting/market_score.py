class MarketScore:


    def __init__(
        self,
        min_score=3
    ):

        self.min_score = min_score



    def is_valid(
        self,
        score
    ):


        return score >= self.min_score