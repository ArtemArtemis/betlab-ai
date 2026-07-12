from collections import defaultdict

from src.config.model_config import MODEL_CONFIG
from src.models.elo import EloRating


class EloAttackDefence:
    """
    Экспериментальная модель рейтингов команды.

    Общий рейтинг делегируется существующему EloRating,
    поэтому контрольная формула Elo не изменяется.

    Attack и defence хранятся как отклонения от нуля:
        attack > 0  — команда забивает больше базового уровня;
        defence > 0 — команда пропускает меньше базового уровня.
    """

    def __init__(
        self,
        expected_goals=1.4,
        attack_defence_learning_rate=0.05,
    ):
        if expected_goals <= 0:
            raise ValueError(
                "expected_goals должен быть больше нуля."
            )

        if attack_defence_learning_rate <= 0:
            raise ValueError(
                "attack_defence_learning_rate "
                "должен быть больше нуля."
            )

        self.overall_elo = EloRating()

        self.k_factor = MODEL_CONFIG[
            "k_factor"
        ]

        self.expected_goals = float(
            expected_goals
        )

        self.learning_rate = float(
            attack_defence_learning_rate
        )

        self.attack_ratings = defaultdict(
            float
        )

        self.defence_ratings = defaultdict(
            float
        )

    def get_overall(
        self,
        team
    ):
        return self.overall_elo.get_rating(
            team
        )

    def get_attack(
        self,
        team
    ):
        return self.attack_ratings[
            team
        ]

    def get_defence(
        self,
        team
    ):
        return self.defence_ratings[
            team
        ]

    def get_team(
        self,
        team
    ):
        return {
            "overall": self.get_overall(
                team
            ),
            "attack": self.get_attack(
                team
            ),
            "defence": self.get_defence(
                team
            ),
        }

    def update(
        self,
        home,
        away,
        result,
        home_goals,
        away_goals
    ):
        """
        Обновляет общий Elo через контрольный EloRating.

        Attack и defence обновляются только после матча.
        Это не создаёт утечки будущих данных.
        """

        goal_difference = (
            home_goals
            -
            away_goals
        )

        self.overall_elo.update(
            home,
            away,
            result,
            goal_difference
        )

        rating_step = (
            self.k_factor
            *
            self.learning_rate
        )

        home_attack_error = (
            home_goals
            -
            self.expected_goals
        )

        away_attack_error = (
            away_goals
            -
            self.expected_goals
        )

        home_defence_error = (
            self.expected_goals
            -
            away_goals
        )

        away_defence_error = (
            self.expected_goals
            -
            home_goals
        )

        self.attack_ratings[
            home
        ] += (
            rating_step
            *
            home_attack_error
        )

        self.attack_ratings[
            away
        ] += (
            rating_step
            *
            away_attack_error
        )

        self.defence_ratings[
            home
        ] += (
            rating_step
            *
            home_defence_error
        )

        self.defence_ratings[
            away
        ] += (
            rating_step
            *
            away_defence_error
        )