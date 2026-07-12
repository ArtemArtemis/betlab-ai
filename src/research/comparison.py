class ExperimentComparison:


    def __init__(self):

        self.experiments = []



    def add(
        self,
        name,
        result
    ):

        self.experiments.append(
            {
                "name": name,
                **result
            }
        )



    def show(self):

        print(
            "\n================================"
        )

        print(
            "RESEARCH COMPARISON"
        )

        print(
            "================================"
        )


        sorted_results = sorted(
            self.experiments,
            key=lambda x: x["roi"],
            reverse=True
        )


        for index, item in enumerate(
            sorted_results,
            start=1
        ):

            print()

            print(
                f"{index}. "
                f"{item['name']}"
            )

            print(
                f"Bets: {item['bets']}"
            )

            print(
                f"Profit: "
                f"{item['profit']:+.2f}"
            )

            print(
                f"ROI: "
                f"{item['roi']:+.2f}%"
            )


        print(
            "\nWinner:"
        )

        print(
            sorted_results[0]["name"]
        )