class BettingAnalyzer:


    def __init__(self, bets):

        self.bets = bets



    def summary(self):

        total = len(self.bets)


        if total == 0:

            print("No bets")

            return


        wins = sum(
            1
            for bet in self.bets
            if bet["win"]
        )


        losses = total - wins


        profit = sum(
            bet["profit"]
            for bet in self.bets
        )


        roi = (
            profit
            /
            (total * 10)
        )


        print("\n===== BETTING SUMMARY =====")


        print(
            f"Bets: {total}"
        )

        print(
            f"Wins: {wins}"
        )

        print(
            f"Losses: {losses}"
        )

        print(
            f"Winrate: {wins / total:.2%}"
        )

        print(
            f"Profit: {profit:.2f}"
        )

        print(
            f"ROI: {roi:.2%}"
        )



    def analyze_edge(self):


        print("\n===== EDGE ANALYSIS =====")


        ranges = [

            ("5-10%", 0.05, 0.10),

            ("10-20%", 0.10, 0.20),

            ("20%+", 0.20, 1.0)

        ]


        for name, low, high in ranges:


            bets = [

                bet

                for bet in self.bets

                if low <= bet["edge"] < high

            ]


            if len(bets) == 0:

                continue


            profit = sum(

                bet["profit"]

                for bet in bets

            )


            wins = sum(

                1

                for bet in bets

                if bet["win"]

            )


            print(
                f"""
Edge {name}

Bets:
{len(bets)}

Wins:
{wins}

Profit:
{profit:.2f}
"""
            )