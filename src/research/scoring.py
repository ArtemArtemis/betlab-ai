class ResearchScore:


    def calculate(
        self,
        result
    ):

        roi = result["roi"]

        bets = result["bets"]

        profitable_seasons = (
            result.get(
                "profitable_seasons",
                0
            )
        )

        total_seasons = (
            result.get(
                "total_seasons",
                1
            )
        )


        roi_score = (
            roi
            *
            0.5
        )


        volume_score = min(
            bets / 100,
            5
        )


        stability_score = (
            profitable_seasons
            /
            total_seasons
            *
            5
        )


        score = (
            roi_score
            +
            volume_score
            +
            stability_score
        )


        return round(
            score,
            2
        )