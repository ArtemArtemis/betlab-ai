class MarketScoreFilter:


    def __init__(
        self,
        min_odds=3.0,
        max_odds=6.0,
        min_edge=0.09,
        max_edge=0.10
    ):

        self.min_odds = min_odds
        self.max_odds = max_odds

        self.min_edge = min_edge
        self.max_edge = max_edge



    def is_valid(
        self,
        odds,
        edge
    ):


        if odds is None:
            return False


        if edge is None:
            return False



        return (

            self.min_odds <= odds <= self.max_odds

            and

            self.min_edge <= edge <= self.max_edge

        )