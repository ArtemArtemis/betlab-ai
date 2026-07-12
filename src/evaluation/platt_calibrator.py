import math

import numpy as np


class PlattCalibrator:
    """
    Калибрует вероятности через логистическое преобразование:

        calibrated_probability =
            sigmoid(
                coefficient * logit(probability)
                + intercept
            )

    Обучение выполняется методом Ньютона.
    """

    def __init__(
        self,
        max_iterations=100,
        tolerance=1e-8,
        regularization=1e-6
    ):
        self.max_iterations = max_iterations
        self.tolerance = tolerance
        self.regularization = regularization

        self.coefficient = 1.0
        self.intercept = 0.0
        self.is_fitted = False

    @staticmethod
    def _clip_probability(probability):

        epsilon = 1e-6

        return min(
            max(float(probability), epsilon),
            1.0 - epsilon
        )

    @classmethod
    def _logit(cls, probability):

        probability = cls._clip_probability(
            probability
        )

        return math.log(
            probability
            /
            (1.0 - probability)
        )

    @staticmethod
    def _sigmoid(value):

        if value >= 0:

            exponent = math.exp(
                -value
            )

            return 1.0 / (
                1.0 + exponent
            )

        exponent = math.exp(
            value
        )

        return exponent / (
            1.0 + exponent
        )

    def fit(self, probabilities, actuals):

        if len(probabilities) != len(actuals):
            raise ValueError(
                "Количество probabilities и actuals "
                "должно совпадать."
            )

        if len(probabilities) == 0:
            raise ValueError(
                "Нельзя обучить калибратор "
                "на пустых данных."
            )

        x_values = np.array(
            [
                self._logit(probability)
                for probability in probabilities
            ],
            dtype=float
        )

        y_values = np.array(
            actuals,
            dtype=float
        )

        design_matrix = np.column_stack(
            [
                x_values,
                np.ones(
                    len(x_values)
                ),
            ]
        )

        parameters = np.array(
            [
                self.coefficient,
                self.intercept,
            ],
            dtype=float
        )

        identity_matrix = np.eye(
            2
        )

        for _ in range(
            self.max_iterations
        ):

            linear_values = (
                design_matrix
                @
                parameters
            )

            predicted_values = np.array(
                [
                    self._sigmoid(value)
                    for value in linear_values
                ]
            )

            weights = (
                predicted_values
                *
                (
                    1.0
                    -
                    predicted_values
                )
            )

            weights = np.maximum(
                weights,
                1e-9
            )

            gradient = (
                design_matrix.T
                @
                (
                    predicted_values
                    -
                    y_values
                )
            )

            gradient += (
                self.regularization
                *
                parameters
            )

            hessian = (
                design_matrix.T
                @
                (
                    design_matrix
                    *
                    weights[:, np.newaxis]
                )
            )

            hessian += (
                self.regularization
                *
                identity_matrix
            )

            try:

                parameter_change = np.linalg.solve(
                    hessian,
                    gradient
                )

            except np.linalg.LinAlgError as error:

                raise RuntimeError(
                    "Не удалось обучить "
                    "PlattCalibrator."
                ) from error

            parameters -= parameter_change

            if np.max(
                np.abs(
                    parameter_change
                )
            ) < self.tolerance:
                break

        self.coefficient = float(
            parameters[0]
        )

        self.intercept = float(
            parameters[1]
        )

        self.is_fitted = True

        return self

    def predict(self, probability):

        if not self.is_fitted:
            raise RuntimeError(
                "Калибратор ещё не обучен."
            )

        logit_probability = self._logit(
            probability
        )

        calibrated_probability = self._sigmoid(
            self.coefficient
            *
            logit_probability
            +
            self.intercept
        )

        return calibrated_probability

    def predict_many(self, probabilities):

        return [
            self.predict(
                probability
            )
            for probability in probabilities
        ]

    def get_parameters(self):

        if not self.is_fitted:
            raise RuntimeError(
                "Калибратор ещё не обучен."
            )

        return {
            "coefficient": self.coefficient,
            "intercept": self.intercept,
        }