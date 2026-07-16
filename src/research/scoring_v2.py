class ResearchScoreV2:


    def calculate(
        self,
        roi,
        profit,
        bets,
        profitable_seasons,
        total_seasons
    ):


        roi_score = roi * 10


        profit_score = (
            profit / 100
        )


        sample_score = min(
            bets / 300,
            1
        ) * 2


        stability_score = (
            profitable_seasons
            /
            total_seasons
            *
            3
        )


        score = (
            roi_score
            +
            profit_score
            +
            sample_score
            +
            stability_score
        )


        return round(
            score,
            2
        )