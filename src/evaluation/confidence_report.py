class ConfidenceReport:


    def generate(
        self,
        results
    ):


        print(
            "\n=============================="
        )

        print(
            "MARKET SCORE CONFIDENCE REPORT"
        )

        print(
            "=============================="
        )


        print(
            f"Seasons tested: "
            f"{results['season_count']}"
        )


        print(
            f"Total bets: "
            f"{results['total_bets']}"
        )


        print(
            f"Wins: "
            f"{results['wins']}"
        )


        print(
            f"Win rate: "
            f"{results['win_rate']}%"
        )


        print(
            f"Profit: "
            f"{results['profit']}"
        )


        print(
            f"ROI: "
            f"{results['roi']}%"
        )


        print(
            f"Positive seasons: "
            f"{results['profitable_seasons']}/"
            f"{results['season_count']}"
        )


        if (
            results["profitable_seasons"]
            ==
            results["season_count"]
            and
            results["roi"] > 10
        ):

            print(
                "STATUS: STRONG"
            )


        elif results["roi"] > 0:

            print(
                "STATUS: PROMISING"
            )


        else:

            print(
                "STATUS: WEAK"
            )