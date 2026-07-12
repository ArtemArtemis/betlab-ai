import pandas as pd

from src.features.football_features import FootballFeatures
from src.backtesting.walk_forward import WalkForwardBacktester


SEASONS = {
    "2023/24": "data/raw/premier_league_2023_24.csv",
    "2024/25": "data/raw/premier_league_2024_25.csv"
}


def calculate_result(bets):

    total_bets = len(bets)

    if total_bets == 0:

        return {
            "bets": 0,
            "wins": 0,
            "profit": 0,
            "roi": 0
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
    )


    return {
        "bets": total_bets,
        "wins": wins,
        "profit": round(
            profit,
            2
        ),
        "roi": round(
            roi * 100,
            2
        )
    }


def main():

    results = []


    print(
        "\n===== MULTI SEASON BACKTEST ====="
    )


    for season, file_path in SEASONS.items():

        print(
            f"\nRunning season {season}..."
        )


        raw_df = pd.read_csv(
            file_path
        )


        features = FootballFeatures(
            raw_df
        )


        prepared_df = features.prepare()


        walk_forward = WalkForwardBacktester()


        bets = walk_forward.run(
            prepared_df
        )


        result = calculate_result(
            bets
        )


        result["season"] = season

        results.append(
            result
        )


    print(
        "\n===== MULTI SEASON RESULTS ====="
    )


    for result in results:

        print(
            f"\nSeason: {result['season']}"
        )

        print(
            f"Bets: {result['bets']}"
        )

        print(
            f"Wins: {result['wins']}"
        )

        print(
            f"Profit: {result['profit']:.2f}"
        )

        print(
            f"ROI: {result['roi']:.2f}%"
        )


    total_bets = sum(
        result["bets"]
        for result in results
    )


    total_profit = sum(
        result["profit"]
        for result in results
    )


    total_staked = sum(
        result["bets"]
        for result in results
    ) * 10


    combined_roi = (
        total_profit
        /
        total_staked
        *
        100
        if total_staked > 0
        else 0
    )


    profitable_seasons = sum(
        1
        for result in results
        if result["profit"] > 0
    )


    print(
        "\n===== COMBINED RESULT ====="
    )

    print(
        f"Total bets: {total_bets}"
    )

    print(
        f"Total profit: {total_profit:.2f}"
    )

    print(
        f"Combined ROI: {combined_roi:.2f}%"
    )

    print(
        f"Profitable seasons: "
        f"{profitable_seasons}/{len(results)}"
    )


if __name__ == "__main__":

    main()