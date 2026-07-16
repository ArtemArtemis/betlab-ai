class DynamicStake:


    def __init__(
        self,
        base_stake=10
    ):

        self.base_stake = base_stake



    def fixed(
        self
    ):

        return self.base_stake



    def edge_based(
        self,
        edge
    ):

        if edge < 0.07:

            multiplier = 0.5


        elif edge < 0.10:

            multiplier = 1


        elif edge < 0.15:

            multiplier = 1.5


        else:

            multiplier = 2



        return round(
            self.base_stake * multiplier,
            2
        )



    def kelly_fraction(
        self,
        probability,
        odds,
        fraction=0.25
    ):

        if odds <= 1:

            return self.base_stake


        q = 1 - probability


        kelly = (

            (
                probability * odds - 1
            )
            /
            (
                odds - 1
            )

        )


        stake = (
            self.base_stake
            *
            kelly
            *
            fraction
        )


        if stake <= 0:

            return self.base_stake * 0.5


        return round(
            stake,
            2
        )