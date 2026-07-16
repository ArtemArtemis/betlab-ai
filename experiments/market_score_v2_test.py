from src.betting.market_score_v2 import MarketScoreV2



def run():


    model = MarketScoreV2()


    tests = [

        {
            "odds": 3.5,
            "edge": 0.095
        },

        {
            "odds": 5.8,
            "edge": 0.11
        },

        {
            "odds": 2.4,
            "edge": 0.09
        },

        {
            "odds": 4.5,
            "edge": 0.115
        },

    ]


    for t in tests:

        score = model.calculate_score(
            t["odds"],
            t["edge"]
        )


        valid = model.is_valid(
            t["odds"],
            t["edge"]
        )


        print(
            t,
            "SCORE:",
            score,
            "VALID:",
            valid
        )



if __name__ == "__main__":

    run()