from src.config.model_config import MODEL_CONFIG


class MarketScore:


    def __init__(self):

        self.min_odds = (
            MODEL_CONFIG["market_score_min_odds"]
        )

        self.max_odds = (
            MODEL_CONFIG["market_score_max_odds"]
        )

        self.min_edge = (
            MODEL_CONFIG["market_score_min_edge"]
        )

        self.max_edge = (
            MODEL_CONFIG["market_score_max_edge"]
        )


    def calculate(
        self,
        odds,
        edge
    ):

        score = 0


        if self.min_odds <= odds <= self.max_odds:
            score += 1


        if self.min_edge <= edge <= self.max_edge:
            score += 1


        return score



    def is_valid(
        self,
        odds,
        edge
    ):

        score = self.calculate(
            odds,
            edge
        )


        return score == 2