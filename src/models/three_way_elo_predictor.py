import math

from src.config.model_config import MODEL_CONFIG


class ThreeWayEloPredictor:
    """
    Экспериментальная трёхисходная Elo-модель.

    Использует расширение Davidson для распределения
    вероятности между тремя исходами:

    - победа хозяев;
    - ничья;
    - победа гостей.

    Контрольный EloPredictor не изменяется.
    """

    def __init__(self, draw_factor=0.7):

        if draw_factor <= 0:
            raise ValueError(
                "draw_factor должен быть больше нуля."
            )

        self.home_advantage = MODEL_CONFIG[
            "home_advantage"
        ]

        self.form_weight = MODEL_CONFIG[
            "form_weight"
        ]

        self.draw_factor = draw_factor

    def predict(
        self,
        home_rating,
        away_rating,
        form_difference=0
    ):
        adjusted_home_rating = (
            home_rating
            +
            self.home_advantage
            +
            (
                form_difference
                *
                self.form_weight
            )
        )

        home_strength = 10 ** (
            adjusted_home_rating / 400
        )

        away_strength = 10 ** (
            away_rating / 400
        )

        draw_strength = (
            self.draw_factor
            *
            math.sqrt(
                home_strength
                *
                away_strength
            )
        )

        total_strength = (
            home_strength
            +
            draw_strength
            +
            away_strength
        )

        home_probability = (
            home_strength
            /
            total_strength
        )

        draw_probability = (
            draw_strength
            /
            total_strength
        )

        away_probability = (
            away_strength
            /
            total_strength
        )

        return {
            "home_win": round(
                home_probability,
                3
            ),
            "draw": round(
                draw_probability,
                3
            ),
            "away_win": round(
                away_probability,
                3
            )
        }