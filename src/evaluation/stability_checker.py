class StabilityChecker:


    def __init__(self):

        self.results = []



    def add_result(
        self,
        season,
        bets,
        wins,
        profit,
        roi
    ):

        self.results.append(
            {
                "season": season,
                "bets": bets,
                "wins": wins,
                "profit": profit,
                "roi": roi
            }
        )



    def summary(self):

        total_bets = sum(
            x["bets"]
            for x in self.results
        )

        total_profit = sum(
            x["profit"]
            for x in self.results
        )


        total_wins = sum(
            x["wins"]
            for x in self.results
        )


        roi = (
            total_profit /
            (total_bets * 10)
            * 100
            if total_bets
            else 0
        )


        profitable_seasons = sum(
            1
            for x in self.results
            if x["profit"] > 0
        )


        return {

            "total_bets": total_bets,

            "wins": total_wins,

            "win_rate":
                round(
                    total_wins /
                    total_bets *
                    100,
                    2
                )
                if total_bets else 0,


            "profit":
                round(
                    total_profit,
                    2
                ),


            "roi":
                round(
                    roi,
                    2
                ),


            "profitable_seasons":
                profitable_seasons,

            "season_count":
                len(self.results)
        }