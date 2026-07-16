class RiskAdjustedStake:


    def __init__(
        self,
        base_stake=10,
        starting_bankroll=1000
    ):

        self.base_stake = base_stake

        self.starting_bankroll = starting_bankroll

        self.peak_bankroll = starting_bankroll



    def update_peak(
        self,
        bankroll
    ):

        if bankroll > self.peak_bankroll:

            self.peak_bankroll = bankroll



    def get_multiplier(
        self,
        bankroll
    ):

        drawdown = (

            self.peak_bankroll - bankroll

        ) / self.peak_bankroll



        if drawdown >= 0.30:

            return 0.25


        if drawdown >= 0.20:

            return 0.50


        if drawdown >= 0.10:

            return 0.75


        return 1.0



    def get_stake(
        self,
        edge,
        bankroll
    ):


        # базовый Dynamic Stake B

        if edge < 0.07:

            multiplier = 0.5


        elif edge < 0.10:

            multiplier = 1.0


        elif edge < 0.15:

            multiplier = 2.0


        else:

            multiplier = 3.0



        risk_multiplier = (
            self.get_multiplier(
                bankroll
            )
        )


        stake = (

            self.base_stake

            *

            multiplier

            *

            risk_multiplier

        )


        return round(
            stake,
            2
        )