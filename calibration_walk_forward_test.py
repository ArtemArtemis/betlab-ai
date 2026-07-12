import pandas as pd

from src.evaluation.platt_calibrator import (
    PlattCalibrator,
)
from src.evaluation.probability_analyzer import (
    ProbabilityAnalyzer,
)


PREDICTION_FILE = (
    "data/processed/"
    "probability_analysis.csv"
)


WALK_FORWARD_TESTS = [
    {
        "name": (
            "Train 2022/23 -> "
            "Test 2023/24"
        ),
        "train_seasons": [
            "2022/23",
        ],
        "test_season": "2023/24",
    },
    {
        "name": (
            "Train 2022/23 + 2023/24 -> "
            "Test 2024/25"
        ),
        "train_seasons": [
            "2022/23",
            "2023/24",
        ],
        "test_season": "2024/25",
    },
]


def load_records():

    dataframe = pd.read_csv(
        PREDICTION_FILE
    )

    required_columns = [
        "season",
        "probability",
        "actual",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in dataframe.columns
    ]

    if missing_columns:
        raise ValueError(
            "Missing required columns: "
            +
            ", ".join(
                missing_columns
            )
        )

    return dataframe


def dataframe_to_records(
    dataframe,
    probability_column
):

    records = []

    for _, row in dataframe.iterrows():

        records.append(
            {
                "probability": float(
                    row[
                        probability_column
                    ]
                ),
                "actual": int(
                    row["actual"]
                ),
            }
        )

    return records


def print_comparison(
    original_summary,
    calibrated_summary
):

    brier_change = (
        calibrated_summary[
            "brier_score"
        ]
        -
        original_summary[
            "brier_score"
        ]
    )

    log_loss_change = (
        calibrated_summary[
            "log_loss"
        ]
        -
        original_summary[
            "log_loss"
        ]
    )

    calibration_change = (
        calibrated_summary[
            "mean_absolute_calibration_error"
        ]
        -
        original_summary[
            "mean_absolute_calibration_error"
        ]
    )

    print(
        "\n===== OUT OF SAMPLE COMPARISON ====="
    )

    print(
        "Brier Score:"
    )

    print(
        "  Original:   "
        f"{original_summary['brier_score']:.4f}"
    )

    print(
        "  Calibrated: "
        f"{calibrated_summary['brier_score']:.4f}"
    )

    print(
        "  Change:     "
        f"{brier_change:+.4f}"
    )

    print(
        "\nLog Loss:"
    )

    print(
        "  Original:   "
        f"{original_summary['log_loss']:.4f}"
    )

    print(
        "  Calibrated: "
        f"{calibrated_summary['log_loss']:.4f}"
    )

    print(
        "  Change:     "
        f"{log_loss_change:+.4f}"
    )

    print(
        "\nMean absolute calibration error:"
    )

    print(
        "  Original:   "
        f"{original_summary['mean_absolute_calibration_error']:.2%}"
    )

    print(
        "  Calibrated: "
        f"{calibrated_summary['mean_absolute_calibration_error']:.2%}"
    )

    print(
        "  Change:     "
        f"{calibration_change:+.2%}"
    )

    improved_metrics = sum(
        [
            brier_change < 0,
            log_loss_change < 0,
            calibration_change < 0,
        ]
    )

    print(
        "\nImproved metrics: "
        f"{improved_metrics}/3"
    )

    return {
        "brier_change": brier_change,
        "log_loss_change": log_loss_change,
        "calibration_change": calibration_change,
        "improved_metrics": improved_metrics,
    }


def run_walk_forward_test(
    dataframe,
    test_config,
    analyzer
):

    print(
        "\n\n========================================"
    )

    print(
        test_config["name"]
    )

    print(
        "========================================"
    )

    train_dataframe = dataframe[
        dataframe["season"].isin(
            test_config[
                "train_seasons"
            ]
        )
    ].copy()

    test_dataframe = dataframe[
        dataframe["season"]
        ==
        test_config["test_season"]
    ].copy()

    if train_dataframe.empty:
        raise ValueError(
            "Training dataframe is empty."
        )

    if test_dataframe.empty:
        raise ValueError(
            "Test dataframe is empty."
        )

    calibrator = PlattCalibrator()

    calibrator.fit(
        probabilities=(
            train_dataframe[
                "probability"
            ].tolist()
        ),
        actuals=(
            train_dataframe[
                "actual"
            ].tolist()
        ),
    )

    parameters = (
        calibrator.get_parameters()
    )

    print(
        "\nCalibration parameters:"
    )

    print(
        "Coefficient: "
        f"{parameters['coefficient']:.6f}"
    )

    print(
        "Intercept: "
        f"{parameters['intercept']:.6f}"
    )

    test_dataframe[
        "calibrated_probability"
    ] = calibrator.predict_many(
        test_dataframe[
            "probability"
        ].tolist()
    )

    original_records = dataframe_to_records(
        test_dataframe,
        "probability"
    )

    calibrated_records = (
        dataframe_to_records(
            test_dataframe,
            "calibrated_probability"
        )
    )

    original_summary = (
        analyzer.print_report(
            original_records,
            (
                "ORIGINAL PROBABILITIES: "
                +
                test_config[
                    "test_season"
                ]
            )
        )
    )

    calibrated_summary = (
        analyzer.print_report(
            calibrated_records,
            (
                "CALIBRATED PROBABILITIES: "
                +
                test_config[
                    "test_season"
                ]
            )
        )
    )

    comparison = print_comparison(
        original_summary,
        calibrated_summary
    )

    return {
        "name": test_config["name"],
        "test_season": (
            test_config[
                "test_season"
            ]
        ),
        "coefficient": parameters[
            "coefficient"
        ],
        "intercept": parameters[
            "intercept"
        ],
        "original": original_summary,
        "calibrated": calibrated_summary,
        "comparison": comparison,
        "output_dataframe": (
            test_dataframe
        ),
    }


def main():

    print(
        "\n===== CALIBRATION WALK FORWARD TEST ====="
    )

    dataframe = load_records()

    analyzer = ProbabilityAnalyzer(
        bin_size=0.10
    )

    test_results = []

    for test_config in WALK_FORWARD_TESTS:

        result = run_walk_forward_test(
            dataframe=dataframe,
            test_config=test_config,
            analyzer=analyzer
        )

        test_results.append(
            result
        )

    output_dataframes = [
        result[
            "output_dataframe"
        ]
        for result in test_results
    ]

    combined_output = pd.concat(
        output_dataframes,
        ignore_index=True
    )

    output_file = (
        "data/processed/"
        "calibration_walk_forward.csv"
    )

    combined_output.to_csv(
        output_file,
        index=False
    )

    print(
        "\n\n===== FINAL CALIBRATION SUMMARY ====="
    )

    for result in test_results:

        print(
            "\n"
            +
            result["name"]
        )

        print(
            "Original Brier: "
            f"{result['original']['brier_score']:.4f}"
        )

        print(
            "Calibrated Brier: "
            f"{result['calibrated']['brier_score']:.4f}"
        )

        print(
            "Original Log Loss: "
            f"{result['original']['log_loss']:.4f}"
        )

        print(
            "Calibrated Log Loss: "
            f"{result['calibrated']['log_loss']:.4f}"
        )

        print(
            "Original Calibration Error: "
            f"{result['original']['mean_absolute_calibration_error']:.2%}"
        )

        print(
            "Calibrated Calibration Error: "
            f"{result['calibrated']['mean_absolute_calibration_error']:.2%}"
        )

        print(
            "Improved metrics: "
            f"{result['comparison']['improved_metrics']}/3"
        )

    print(
        "\nSaved calibrated predictions:"
    )

    print(
        output_file
    )


if __name__ == "__main__":
    main()