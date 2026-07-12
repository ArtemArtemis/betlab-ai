from copy import deepcopy

import pandas as pd

from src.backtesting.walk_forward import WalkForwardBacktester
from src.config.model_config import MODEL_CONFIG
from src.features.football_features import FootballFeatures


TEST_PARAMETERS = {
    "form_weight": 40,
    "min_edge": 0.06,
    "max_edge": 0.10,
}


def load_season(file_path):
    """
    Загружает исходный CSV и применяет
    существующий FootballFeatures.
    """

    raw_dataframe = pd.read_csv(file_path)

    features = FootballFeatures(raw_dataframe)

    prepared_dataframe = features.prepare()

    return prepared_dataframe


def calculate_result(bets):
    """
    Рассчитывает основные показатели бэктеста.
    """

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
        if bet.get("win") is True
    )

    profit = sum(
        float(bet.get("profit", 0.0))
        for bet in bets
    )

    total_stake = sum(
        float(bet.get("stake", 0.0))
        for bet in bets
    )

    roi = (
        profit / total_stake * 100
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


def main():
    print(
        "\n===== OUT OF SAMPLE TEST ====="
    )

    print(
        "\nFrozen parameters:"
    )
    print(
        f"form_weight = "
        f"{TEST_PARAMETERS['form_weight']}"
    )
    print(
        f"min_edge = "
        f"{TEST_PARAMETERS['min_edge']:.2f}"
    )
    print(
        f"max_edge = "
        f"{TEST_PARAMETERS['max_edge']:.2f}"
    )

    dataframe = load_season(
        "data/raw/premier_league_2022_23.csv"
    )

    original_config = deepcopy(MODEL_CONFIG)

    try:
        MODEL_CONFIG["form_weight"] = (
            TEST_PARAMETERS["form_weight"]
        )
        MODEL_CONFIG["min_edge"] = (
            TEST_PARAMETERS["min_edge"]
        )
        MODEL_CONFIG["max_edge"] = (
            TEST_PARAMETERS["max_edge"]
        )

        backtester = WalkForwardBacktester()

        bets = backtester.run(
            dataframe.copy()
        )

        result = calculate_result(bets)

    finally:
        MODEL_CONFIG.clear()
        MODEL_CONFIG.update(original_config)

    print(
        "\n===== OUT OF SAMPLE RESULT ====="
    )
    print(
        "Season: 2022/23"
    )
    print(
        f"Bets: {result['bets']}"
    )
    print(
        f"Wins: {result['wins']}"
    )
    print(
        f"Profit: {result['profit']:+.2f}"
    )
    print(
        f"Total stake: "
        f"{result['total_stake']:.2f}"
    )
    print(
        f"ROI: {result['roi']:+.2f}%"
    )


if __name__ == "__main__":
    main()