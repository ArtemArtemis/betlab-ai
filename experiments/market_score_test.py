import pandas as pd


from src.collectors.football_data import FootballDataCollector

from src.features.football_features import FootballFeatures


from src.backtesting.risk_adjusted_walk_forward import (
    RiskAdjustedWalkForwardBacktester
)


from src.models.market_regime import MarketRegime

from src.betting.market_score import MarketScore



SEASONS = [

    "2022_23",
    "2023_24",
    "2024_25"

]



def prepare_data(
    season
):


    path = (
        f"data/raw/"
        f"premier_league_{season}.csv"
    )


    print(
        f"Loading {path}"
    )


    df = pd.read_csv(
        path
    )


    features = FootballFeatures(
        df
    )


    return features.prepare()



def filter_bets(
    bets
):


    regime = MarketRegime()

    scorer = MarketScore(
        min_score=3
    )


    filtered = []


    for bet in bets:


        score = regime.get_score(

            bet["odds"],

            bet["edge"]

        )


        if scorer.is_valid(score):

            bet["market_score"] = score

            filtered.append(
                bet
            )


    return filtered




def run():


    all_results = []


    for season in SEASONS:


        print("=" * 40)

        print(
            season
        )

        print("=" * 40)


        df = prepare_data(
            season
        )


        model = RiskAdjustedWalkForwardBacktester()


        bets = model.run(
            df
        )


        filtered = filter_bets(
            bets
        )


        profit = sum(

            x["profit"]

            for x in filtered

        )


        wins = sum(

            1

            for x in filtered

            if x["win"]

        )


        count = len(
            filtered
        )


        roi = (

            profit /
            sum(
                x["stake"]
                for x in filtered
            )
            *
            100

            if count > 0

            else 0

        )


        result = {


            "season":

            season,


            "bets":

            count,


            "wins":

            wins,


            "profit":

            round(
                profit,
                2
            ),


            "roi":

            round(
                roi,
                2
            )

        }


        all_results.append(
            result
        )


        print(
            result
        )



    print()

    print(
        "FINAL"
    )

    print(
        pd.DataFrame(
            all_results
        )
    )




if __name__ == "__main__":

    run()