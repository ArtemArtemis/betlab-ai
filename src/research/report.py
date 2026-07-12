class ExperimentReport:


    def __init__(
        self,
        experiment_name
    ):

        self.experiment_name = (
            experiment_name
        )

        self.results = []



    def add_result(
        self,
        season,
        metrics
    ):

        self.results.append(
            {
                "season": season,
                **metrics
            }
        )



    def summary(self):

        print(
            "\n=============================="
        )

        print(
            f"EXPERIMENT: "
            f"{self.experiment_name}"
        )

        print(
            "=============================="
        )


        total_profit = 0

        total_bets = 0


        for result in self.results:

            print(
                f"\nSeason: "
                f"{result['season']}"
            )

            print(
                f"Bets: "
                f"{result['bets']}"
            )

            print(
                f"Profit: "
                f"{result['profit']:+.2f}"
            )

            print(
                f"ROI: "
                f"{result['roi']:+.2f}%"
            )


            total_profit += (
                result["profit"]
            )

            total_bets += (
                result["bets"]
            )


        total_stake = (
            total_bets
            *
            10
        )


        combined_roi = (
            total_profit
            /
            total_stake
            *
            100
            if total_stake > 0
            else 0
        )


        print(
            "\nTOTAL"
        )

        print(
            f"Bets: {total_bets}"
        )

        print(
            f"Profit: "
            f"{total_profit:+.2f}"
        )

        print(
            f"ROI: "
            f"{combined_roi:+.2f}%"
        )