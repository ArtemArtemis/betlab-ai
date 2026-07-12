import math

import pandas as pd


class ProbabilityAnalyzer:
    """
    Анализирует качество бинарных вероятностей модели.

    Каждый прогноз рассматривается как отдельное событие:

    - вероятность победы хозяев;
    - вероятность победы гостей.

    При ничьей фактический результат равен 0
    и для хозяев, и для гостей.
    """

    def __init__(self, bin_size=0.10):

        if not 0 < bin_size <= 1:
            raise ValueError(
                "bin_size должен быть в диапазоне (0, 1]."
            )

        self.bin_size = bin_size

    @staticmethod
    def _clip_probability(probability):

        epsilon = 1e-15

        return min(
            max(float(probability), epsilon),
            1 - epsilon
        )

    def brier_score(self, records):

        if not records:
            return 0.0

        squared_errors = [
            (
                float(record["probability"])
                -
                int(record["actual"])
            ) ** 2
            for record in records
        ]

        return sum(squared_errors) / len(
            squared_errors
        )

    def log_loss(self, records):

        if not records:
            return 0.0

        losses = []

        for record in records:

            probability = self._clip_probability(
                record["probability"]
            )

            actual = int(
                record["actual"]
            )

            loss = -(
                actual
                *
                math.log(probability)
                +
                (1 - actual)
                *
                math.log(1 - probability)
            )

            losses.append(loss)

        return sum(losses) / len(losses)

    def calibration_table(self, records):

        if not records:
            return pd.DataFrame(
                columns=[
                    "range",
                    "predictions",
                    "average_probability",
                    "actual_win_rate",
                    "calibration_error",
                ]
            )

        rows = []

        number_of_bins = int(
            math.ceil(
                1 / self.bin_size
            )
        )

        for bin_index in range(
            number_of_bins
        ):

            lower_bound = (
                bin_index
                *
                self.bin_size
            )

            upper_bound = min(
                lower_bound
                +
                self.bin_size,
                1.0
            )

            if upper_bound == 1.0:

                bin_records = [
                    record
                    for record in records
                    if (
                        lower_bound
                        <= record["probability"]
                        <= upper_bound
                    )
                ]

            else:

                bin_records = [
                    record
                    for record in records
                    if (
                        lower_bound
                        <= record["probability"]
                        < upper_bound
                    )
                ]

            if not bin_records:
                continue

            average_probability = sum(
                record["probability"]
                for record in bin_records
            ) / len(bin_records)

            actual_win_rate = sum(
                record["actual"]
                for record in bin_records
            ) / len(bin_records)

            calibration_error = (
                average_probability
                -
                actual_win_rate
            )

            rows.append(
                {
                    "range": (
                        f"{lower_bound:.2f}"
                        f"-{upper_bound:.2f}"
                    ),
                    "predictions": len(
                        bin_records
                    ),
                    "average_probability": (
                        average_probability
                    ),
                    "actual_win_rate": (
                        actual_win_rate
                    ),
                    "calibration_error": (
                        calibration_error
                    ),
                }
            )

        return pd.DataFrame(rows)

    def summarize(self, records):

        if not records:
            return {
                "predictions": 0,
                "average_probability": 0.0,
                "actual_win_rate": 0.0,
                "brier_score": 0.0,
                "log_loss": 0.0,
                "mean_absolute_calibration_error": 0.0,
            }

        average_probability = sum(
            record["probability"]
            for record in records
        ) / len(records)

        actual_win_rate = sum(
            record["actual"]
            for record in records
        ) / len(records)

        calibration = self.calibration_table(
            records
        )

        if calibration.empty:

            mean_absolute_calibration_error = (
                0.0
            )

        else:

            weighted_error_sum = sum(
                abs(
                    row[
                        "calibration_error"
                    ]
                )
                *
                row["predictions"]
                for _, row in calibration.iterrows()
            )

            total_predictions = sum(
                calibration[
                    "predictions"
                ]
            )

            mean_absolute_calibration_error = (
                weighted_error_sum
                /
                total_predictions
            )

        return {
            "predictions": len(records),
            "average_probability": (
                average_probability
            ),
            "actual_win_rate": (
                actual_win_rate
            ),
            "brier_score": self.brier_score(
                records
            ),
            "log_loss": self.log_loss(
                records
            ),
            "mean_absolute_calibration_error": (
                mean_absolute_calibration_error
            ),
        }

    def print_report(
        self,
        records,
        title
    ):

        summary = self.summarize(
            records
        )

        calibration = self.calibration_table(
            records
        )

        print(
            "\n========================================"
        )

        print(title)

        print(
            "========================================"
        )

        print(
            f"Predictions: "
            f"{summary['predictions']}"
        )

        print(
            "Average predicted probability: "
            f"{summary['average_probability']:.2%}"
        )

        print(
            "Actual win rate: "
            f"{summary['actual_win_rate']:.2%}"
        )

        print(
            f"Brier Score: "
            f"{summary['brier_score']:.4f}"
        )

        print(
            f"Log Loss: "
            f"{summary['log_loss']:.4f}"
        )

        print(
            "Mean absolute calibration error: "
            f"{summary['mean_absolute_calibration_error']:.2%}"
        )

        print(
            "\nCalibration table:"
        )

        if calibration.empty:

            print(
                "No calibration data."
            )

            return summary

        formatted_table = calibration.copy()

        formatted_table[
            "average_probability"
        ] = formatted_table[
            "average_probability"
        ].map(
            lambda value: f"{value:.2%}"
        )

        formatted_table[
            "actual_win_rate"
        ] = formatted_table[
            "actual_win_rate"
        ].map(
            lambda value: f"{value:.2%}"
        )

        formatted_table[
            "calibration_error"
        ] = formatted_table[
            "calibration_error"
        ].map(
            lambda value: f"{value:+.2%}"
        )

        print(
            formatted_table.to_string(
                index=False
            )
        )

        return summary