class MarketRegime:


    def __init__(self):

        pass



    def odds_score(
        self,
        odds
    ):

        score = 0


        if 3.0 <= odds <= 6.0:

            score += 2


        elif 2.0 <= odds < 3.0:

            score += 1


        elif odds > 6.0:

            score -= 2


        elif odds < 2.0:

            score -= 1


        return score



    def edge_score(
        self,
        edge
    ):

        score = 0


        edge_percent = edge * 100


        if 9 <= edge_percent <= 10:

            score += 2


        elif 10 < edge_percent <= 12:

            score += 1


        elif edge_percent > 12:

            score -= 1


        elif 7 <= edge_percent < 9:

            score += 0


        else:

            score -= 2


        return score



    def get_score(
        self,
        odds,
        edge
    ):


        return (
            self.odds_score(odds)
            +
            self.edge_score(edge)
        )