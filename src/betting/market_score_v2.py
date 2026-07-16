from src.config.model_config import MODEL_CONFIG



class MarketScoreV2:


    def __init__(self):

        self.min_odds = MODEL_CONFIG["market_score_min_odds"]

        self.max_odds = MODEL_CONFIG["market_score_max_odds"]



    def calculate_score(
        self,
        odds,
        edge
    ):

        score = 0


        # хороший диапазон коэффициента
        if (
            self.min_odds
            <= odds
            <= self.max_odds
        ):

            score += 1



        # оптимальный edge
        if (
            0.08
            <= edge
            < 0.10
        ):

            score += 1



        # повышенный edge
        if (
            0.10
            <= edge
            <= 0.12
        ):

            score += 1



        # дополнительный бонус за средний рынок
        if (
            3.0
            <= odds
            <= 5.0
        ):

            score += 1



        return score



    def is_valid(
        self,
        odds,
        edge,
        min_score=2
    ):

        return (
            self.calculate_score(
                odds,
                edge
            )
            >= min_score
        )