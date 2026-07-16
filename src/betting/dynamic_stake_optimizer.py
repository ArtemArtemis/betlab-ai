class DynamicStakeOptimizer:


    VARIANTS = {

        "A": {

            "name": "Balanced",

            "rules": [
                (0.07, 0.5),
                (0.10, 1.0),
                (0.15, 1.5),
                (1.00, 2.0)
            ]

        },


        "B": {

            "name": "Aggressive",

            "rules": [
                (0.07, 0.5),
                (0.10, 1.0),
                (0.15, 2.0),
                (1.00, 3.0)
            ]

        },


        "C": {

            "name": "Conservative",

            "rules": [
                (0.07, 0.25),
                (0.10, 0.5),
                (0.15, 1.0),
                (1.00, 1.5)
            ]

        }

    }



    def __init__(
        self,
        variant="A",
        base_stake=10
    ):

        self.variant = variant

        self.base_stake = base_stake



    def get_stake(
        self,
        edge
    ):

        rules = (
            self.VARIANTS[
                self.variant
            ]["rules"]
        )


        for limit, multiplier in rules:

            if edge < limit:

                return round(
                    self.base_stake * multiplier,
                    2
                )


        return self.base_stake



    # совместимость со старым DynamicStake

    def edge_based(
        self,
        edge
    ):

        return self.get_stake(
            edge
        )