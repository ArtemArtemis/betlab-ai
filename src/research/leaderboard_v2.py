import os
import json

from src.research.scoring_v2 import ResearchScoreV2


class ResearchLeaderboard:


    def __init__(
        self,
        results_path="data/research/results"
    ):

        self.results_path = results_path

        self.results = []

        self.scorer = ResearchScoreV2()



    def load_results(self):

        if not os.path.exists(
            self.results_path
        ):
            return []


        for file in os.listdir(
            self.results_path
        ):

            if not file.endswith(".json"):
                continue


            filepath = os.path.join(
                self.results_path,
                file
            )


            with open(
                filepath,
                "r",
                encoding="utf-8"
            ) as f:

                data = json.load(f)



            result = data.get(
                "results",
                {}
            )


            score = self.scorer.calculate(

                roi=result.get(
                    "roi",
                    0
                ),

                profit=result.get(
                    "profit",
                    0
                ),

                bets=result.get(
                    "bets",
                    0
                ),

                profitable_seasons=result.get(
                    "profitable_seasons",
                    0
                ),

                total_seasons=result.get(
                    "total_seasons",
                    1
                )

            )


            self.results.append(

                {
                    "model":
                        data.get(
                            "experiment",
                            "Unknown"
                        ),

                    "bets":
                        result.get(
                            "bets",
                            0
                        ),

                    "profit":
                        result.get(
                            "profit",
                            0
                        ),

                    "roi":
                        result.get(
                            "roi",
                            0
                        ),

                    "score":
                        score
                }

            )


        return self.results



    def show(self):

        if not self.results:

            self.load_results()



        self.results.sort(
            key=lambda x: x["score"],
            reverse=True
        )


        print(
            "\n================================"
        )

        print(
            "BETLAB AI RESEARCH LEADERBOARD"
        )

        print(
            "================================\n"
        )


        for index, item in enumerate(
            self.results,
            start=1
        ):

            print(
                f"{index}. {item['model']}"
            )

            print(
                f"Bets: {item['bets']}"
            )

            print(
                f"Profit: {item['profit']:+.2f}"
            )

            print(
                f"ROI: {item['roi']:+.2f}%"
            )

            print(
                f"Score V2: {item['score']}"
            )

            print(
                "----------------------------"
            )


        if self.results:

            print(
                "\nWINNER:"
            )

            print(
                self.results[0]["model"]
            )