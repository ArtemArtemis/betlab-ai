from copy import deepcopy

import pandas as pd

from src.config.model_config import MODEL_CONFIG
from src.evaluation.probability_analyzer import (
    ProbabilityAnalyzer,
)
from src.features.football_features import (
    FootballFeatures,
)
from src.models.elo import EloRating
from src.models.elo_predictor import EloPredictor
from src.models.team_form import TeamForm


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


CONTROL_PARAMETERS = {
    "form_weight": 80,
    "min_edge": 0.07,
    "max_edge": 0.12,
}


def load_season(file_path):

    raw_dataframe = pd.read_csv(
        file_path
    )

    return FootballFeatures(
        raw_dataframe
    ).prepare()


def create_prediction_records(
    dataframe,
    season_name
):
    """
    Создаёт прогнозы walk-forward без ставок.

    Рейтинг и форма обновляются только после
    сохранения прогноза текущего матча.
    """

    elo = EloRating()

    team_form = TeamForm()

    predictor = EloPredictor()

    records = []

    dataframe = dataframe.sort_values(
        by="Date"
    )

    for _, match in dataframe.iterrows():

        home_team = match[
            "HomeTeam"
        ]

        away_team = match[
            "AwayTeam"
        ]

        home_rating = elo.get_rating(
            home_team
        )

        away_rating = elo.get_rating(
            away_team
        )

        form_difference = (
            team_form.get_difference(
                home_team,
                away_team
            )
        )

        prediction = predictor.predict(
            home_rating,
            away_rating,
            form_difference
        )

        home_actual = int(
            match["FTHG"]
            >
            match["FTAG"]
        )

        away_actual = int(
            match["FTAG"]
            >
            match["FTHG"]
        )

        records.append(
            {
                "season": season_name,
                "date": match["Date"],
                "team": home_team,
                "opponent": away_team,
                "side": "HOME",
                "probability": prediction[
                    "home_win"
                ],
                "actual": home_actual,
                "was_draw": int(
                    match["FTHG"]
                    ==
                    match["FTAG"]
                ),
            }
        )

        records.append(
            {
                "season": season_name,
                "date": match["Date"],
                "team": away_team,
                "opponent": home_team,
                "side": "AWAY",
                "probability": prediction[
                    "away_win"
                ],
                "actual": away_actual,
                "was_draw": int(
                    match["FTHG"]
                    ==
                    match["FTAG"]
                ),
            }
        )

        if match["FTHG"] > match["FTAG"]:

            result = "H"

        elif match["FTHG"] < match["FTAG"]:

            result = "A"

        else:

            result = "D"

        goal_difference = (
            match["FTHG"]
            -
            match["FTAG"]
        )

        elo.update(
            home_team,
            away_team,
            result,
            goal_difference
        )

        team_form.update(
            home_team,
            away_team,
            result
        )

    return records


def print_draw_analysis(records):

    draw_records = [
        record
        for record in records
        if record["was_draw"] == 1
    ]

    if not draw_records:

        print(
            "\nNo draw records."
        )

        return

    average_probability = sum(
        record["probability"]
        for record in draw_records
    ) / len(draw_records)

    high_confidence_predictions = sum(
        1
        for record in draw_records
        if record["probability"] >= 0.60
    )

    print(
        "\n===== DRAW MATCH ANALYSIS ====="
    )

    print(
        "Side predictions belonging to drawn matches: "
        f"{len(draw_records)}"
    )

    print(
        "Average win probability in drawn matches: "
        f"{average_probability:.2%}"
    )

    print(
        "Predictions >= 60% in drawn matches: "
        f"{high_confidence_predictions}"
    )


def main():

    print(
        "\n===== PROBABILITY ANALYSIS ====="
    )

    print(
        "\nFrozen control parameters:"
    )

    print(
        "form_weight = "
        f"{CONTROL_PARAMETERS['form_weight']}"
    )

    print(
        "min_edge = "
        f"{CONTROL_PARAMETERS['min_edge']:.2f}"
    )

    print(
        "max_edge = "
        f"{CONTROL_PARAMETERS['max_edge']:.2f}"
    )

    original_config = deepcopy(
        MODEL_CONFIG
    )

    all_records = []

    try:

        MODEL_CONFIG["form_weight"] = (
            CONTROL_PARAMETERS[
                "form_weight"
            ]
        )

        MODEL_CONFIG["min_edge"] = (
            CONTROL_PARAMETERS[
                "min_edge"
            ]
        )

        MODEL_CONFIG["max_edge"] = (
            CONTROL_PARAMETERS[
                "max_edge"
            ]
        )

        analyzer = ProbabilityAnalyzer(
            bin_size=0.10
        )

        for (
            season_name,
            file_path
        ) in SEASONS.items():

            print(
                f"\nLoading season "
                f"{season_name}..."
            )

            dataframe = load_season(
                file_path
            )

            season_records = (
                create_prediction_records(
                    dataframe,
                    season_name
                )
            )

            all_records.extend(
                season_records
            )

            analyzer.print_report(
                season_records,
                (
                    "SEASON PROBABILITY REPORT: "
                    f"{season_name}"
                )
            )

        analyzer.print_report(
            all_records,
            "COMBINED PROBABILITY REPORT"
        )

        home_records = [
            record
            for record in all_records
            if record["side"] == "HOME"
        ]

        away_records = [
            record
            for record in all_records
            if record["side"] == "AWAY"
        ]

        analyzer.print_report(
            home_records,
            "HOME PROBABILITY REPORT"
        )

        analyzer.print_report(
            away_records,
            "AWAY PROBABILITY REPORT"
        )

        print_draw_analysis(
            all_records
        )

        output_dataframe = pd.DataFrame(
            all_records
        )

        output_file = (
            "data/processed/"
            "probability_analysis.csv"
        )

        output_dataframe.to_csv(
            output_file,
            index=False
        )

        print(
            "\nSaved prediction records:"
        )

        print(
            output_file
        )

    finally:

        MODEL_CONFIG.clear()

        MODEL_CONFIG.update(
            original_config
        )


if __name__ == "__main__":
    main()