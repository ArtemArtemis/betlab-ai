from src.research.storage import ExperimentStorage


class Leaderboard:


    def __init__(self):

        self.storage = ExperimentStorage()



    def generate(self):

        results = (
            self.storage.load_all()
        )


        if not results:

            print(
                "No experiments found"
            )

            return


        ranking = sorted(
            results,
            key=lambda x:
                x["results"].get(
                    "research_score",
                    0
                ),
            reverse=True
        )


        print(
            "\n================================"
        )

        print(
            "BETLAB AI LEADERBOARD"
        )

        print(
            "================================"
        )


        for index, item in enumerate(
            ranking,
            start=1
        ):

            result = item["results"]


            print()

            print(
                f"{index}. "
                f"{item['experiment']}"
            )

            print(
                f"Model: {item['model']}"
            )

            print(
                f"Bets: {result['bets']}"
            )

            print(
                f"Profit: "
                f"{result['profit']:+.2f}"
            )

            print(
                f"ROI: "
                f"{result['roi']:+.2f}%"
            )


            print(
                f"Research Score: "
                f"{result.get('research_score',0):.2f}"
            )           

            print(
                f"Stability: "
                f"{result.get('profitable_seasons',0)}/"
                f"{result.get('total_seasons',0)}"
            )


        print(
            "\n================================"
        )

        print(
            "Winner:"
        )

        print(
            ranking[0]["experiment"]
        )