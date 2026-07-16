from src.betting.market_score_filter import (
    MarketScoreFilter
)



def run():


    market_filter = MarketScoreFilter()


    tests = [

        {
            "odds": 3.50,
            "edge": 0.095
        },

        {
            "odds": 2.50,
            "edge": 0.095
        },

        {
            "odds": 4.50,
            "edge": 0.120
        },

        {
            "odds": 5.90,
            "edge": 0.092
        }

    ]



    for test in tests:


        result = market_filter.is_valid(

            test["odds"],

            test["edge"]

        )


        print(
            test,
            "=>",
            result
        )



if __name__ == "__main__":

    run()