class BettingMetrics:


    def calculate(
        self,
        bets
    ):

        total_bets = len(
            bets
        )


        if total_bets == 0:

            return {
                "bets":0,
                "wins":0,
                "profit":0,
                "roi":0
            }


        wins = sum(
            1
            for bet in bets
            if bet["win"]
        )


        profit = sum(
            bet["profit"]
            for bet in bets
        )


        total_stake = sum(
            bet["stake"]
            for bet in bets
        )


        roi = (
            profit
            /
            total_stake
            *
            100
        )


        return {

            "bets": total_bets,

            "wins": wins,

            "win_rate":
                wins / total_bets * 100,

            "profit": profit,

            "roi": roi,

        }