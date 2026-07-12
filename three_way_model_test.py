from copy import deepcopy

import pandas as pd

from src.backtesting.three_way_walk_forward import (
    ThreeWayWalkForwardBacktester,
)
from src.config.model_config import MODEL_CONFIG
from src.features.football_features import FootballFeatures


SEASONS = {
    "2022/23": (
        "data/raw/"
        "premier_league_2022_23.csv"
    ),
    "2023/24": (
        "data/raw/"
        "premier_league_2023_24.csv"
    ),
    "2024/25": (
        "data/raw/"
        "premier_league_2024_25.csv"
    ),
}


PARAMETER_SETS = {
    "Control parameters": {
        "form_weight": 80,
        "min_edge": 0.07,
        "max_edge": 0.12,
    },
    "Stable candidate": {
        "form_weight": 40,
        "min_edge": 0.06,
        "max_edge": 0.10,
    },
}


DRAW_FACTOR = 0.7


def load_season(file_path):

    raw_dataframe = pd.read_csv(
        file_path
    )

    prepared_dataframe = FootballFeatures(
        raw_dataframe
    ).prepare()

    return prepared_dataframe


def calculate_result(bets):

    bets_count = len(bets)

    if bets_count == 0:
        return {
            "bets": 0,
            "wins": 0,
            "profit": 0.0,
            "total_stake": 0.0,
            "roi": 0.0,
        }

    wins = sum(
        1
        for bet in bets
        if bet["win"]
    )

    profit = sum(
        float(bet["profit"])
        for bet in bets
    )

    total_stake = sum(
        float(bet["stake"])
        for bet in bets
    )

    roi = (
        profit
        /
        total_stake
        *
        100
        if total_stake > 0
        else 0.0
    )

    return {
        "bets": bets_count,
        "wins": wins,
        "profit": profit,
        "total_stake": total_stake,
        "roi": roi,
    }


def run_parameter_set(
    parameter_name,
    parameters,
    loaded_seasons
):
    print(
        "\n\n========================================"
    )

    print(
        f"PARAMETER SET: {parameter_name}"
    )

    print(
        "========================================"
    )

    print(
        f"form_weight = "
        f"{parameters['form_weight']}"
    )

    print(
        f"min_edge = "
        f"{parameters['min_edge']:.2f}"
    )

    print(
        f"max_edge = "
        f"{parameters['max_edge']:.2f}"
    )

    print(
        f"draw_factor = {DRAW_FACTOR:.2f}"
    )

    original_config = deepcopy(
        MODEL_CONFIG
    )

    season_results = {}

    try:
        MODEL_CONFIG["form_weight"] = (
            parameters["form_weight"]
        )

        MODEL_CONFIG["min_edge"] = (
            parameters["min_edge"]
        )

        MODEL_CONFIG["max_edge"] = (
            parameters["max_edge"]
        )

        for (
            season_name,
            dataframe
        ) in loaded_seasons.items():

            print(
                f"\nRunning season "
                f"{season_name}..."
            )

            backtester = (
                ThreeWayWalkForwardBacktester(
                    draw_factor=DRAW_FACTOR
                )
            )

            bets = backtester.run(
                dataframe.copy()
            )

            season_results[
                season_name
            ] = calculate_result(
                bets
            )

    finally:
        MODEL_CONFIG.clear()
        MODEL_CONFIG.update(
            original_config
        )

    total_bets = sum(
        result["bets"]
        for result in season_results.values()
    )

    total_wins = sum(
        result["wins"]
        for result in season_results.values()
    )

    total_profit = sum(
        result["profit"]
        for result in season_results.values()
    )

    total_stake = sum(
        result["total_stake"]
        for result in season_results.values()
    )

    combined_roi = (
        total_profit
        /
        total_stake
        *
        100
        if total_stake > 0
        else 0.0
    )

    profitable_seasons = sum(
        1
        for result in season_results.values()
        if result["profit"] > 0
    )

    print(
        "\n===== THREE-WAY MODEL RESULTS ====="
    )

    print(
        f"Parameter set: {parameter_name}"
    )

    for (
        season_name,
        result
    ) in season_results.items():

        print(
            f"\nSeason: {season_name}"
        )

        print(
            f"Bets: {result['bets']}"
        )

        print(
            f"Wins: {result['wins']}"
        )

        print(
            f"Profit: "
            f"{result['profit']:+.2f}"
        )

        print(
            f"ROI: "
            f"{result['roi']:+.2f}%"
        )

    print(
        "\n===== COMBINED RESULT ====="
    )

    print(
        f"Total bets: {total_bets}"
    )

    print(
        f"Total wins: {total_wins}"
    )

    print(
        f"Total profit: "
        f"{total_profit:+.2f}"
    )

    print(
        f"Combined ROI: "
        f"{combined_roi:+.2f}%"
    )

    print(
        "Profitable seasons: "
        f"{profitable_seasons}"
        f"/{len(season_results)}"
    )

    return {
        "parameter_name": parameter_name,
        "season_results": season_results,
        "total_bets": total_bets,
        "total_wins": total_wins,
        "total_profit": total_profit,
        "combined_roi": combined_roi,
        "profitable_seasons": profitable_seasons,
    }


def main():

    print(
        "\n===== THREE-WAY ELO EXPERIMENT ====="
    )

    print(
        "\nLoading seasons..."
    )

    loaded_seasons = {
        season_name: load_season(
            file_path
        )
        for (
            season_name,
            file_path
        ) in SEASONS.items()
    }

    experiment_results = []

    for (
        parameter_name,
        parameters
    ) in PARAMETER_SETS.items():

        result = run_parameter_set(
            parameter_name=parameter_name,
            parameters=parameters,
            loaded_seasons=loaded_seasons
        )

        experiment_results.append(
            result
        )

    print(
        "\n\n===== FINAL COMPARISON ====="
    )

    for result in experiment_results:

        print(
            "\n"
            f"{result['parameter_name']}:"
        )

        print(
            f"Total bets: "
            f"{result['total_bets']}"
        )

        print(
            f"Total profit: "
            f"{result['total_profit']:+.2f}"
        )

        print(
            f"Combined ROI: "
            f"{result['combined_roi']:+.2f}%"
        )

        print(
            "Profitable seasons: "
            f"{result['profitable_seasons']}/3"
        )


if __name__ == "__main__":
    main()