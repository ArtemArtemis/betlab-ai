from src.backtesting.risk_adjusted_walk_forward import (
    RiskAdjustedWalkForwardBacktester
)


class OddsRegimeWalkForward(
    RiskAdjustedWalkForwardBacktester
):


    def __init__(
        self,
        odds_min=None,
        odds_max=None
    ):

        super().__init__()

        self.odds_min = odds_min
        self.odds_max = odds_max



    def check_odds(self, odds):

        if self.odds_min is None:
            return True

        return (
            self.odds_min 
            <= odds 
            <= self.odds_max
        )