from src.config.model_config import MODEL_CONFIG


class AttackDefencePredictor:
    """
    Экспериментальный predictor.

    Контрольная Elo-вероятность дополняется отдельными
    атакующим и оборонительным сигналами.

    Attack и defence являются отклонениями от нуля,
    поэтому базовый рейтинг 1500 не дублируется.
    """

    def __init__(
        self,
        attack_weight=10.0,
        defence_weight=10.0,
    ):
        self.home_advantage = MODEL_CONFIG[
            "home_advantage"
        ]

        self.form_weight = MODEL_CONFIG[
            "form_weight"
        ]

        self.attack_weight = float(
            attack_weight
        )

        self.defence_weight = float(
            defence_weight
        )

    def predict(
        self,
        home_overall,
        away_overall,
        home_attack,
        away_attack,
        home_defence,
        away_defence,
        form_difference=0,
    ):
        home_attack_signal = (
            home_attack
            -
            away_defence
        )

        away_attack_signal = (
            away_attack
            -
            home_defence
        )

        adjusted_home_rating = (
            home_overall
            +
            self.home_advantage
            +
            (
                form_difference
                *
                self.form_weight
            )
            +
            (
                home_attack_signal
                *
                self.attack_weight
            )
        )

        adjusted_away_rating = (
            away_overall
            +
            (
                away_attack_signal
                *
                self.defence_weight
            )
        )

        home_probability = 1 / (
            1
            +
            10 ** (
                (
                    adjusted_away_rating
                    -
                    adjusted_home_rating
                )
                /
                400
            )
        )

        away_probability = (
            1
            -
            home_probability
        )

        return {
            "home_win": round(
                home_probability,
                3
            ),
            "away_win": round(
                away_probability,
                3
            ),
        }