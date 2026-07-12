from src.backtesting.backtester import Backtester
from src.betting.value_detector import ValueDetector
from src.models.attack_defence_predictor import (
    AttackDefencePredictor,
)
from src.models.elo_attack_defence import (
    EloAttackDefence,
)
from src.models.team_form import TeamForm


class AttackDefenceWalkForwardBacktester:
    """
    Экспериментальный walk-forward backtest.

    Контрольный WalkForwardBacktester не изменяется.
    """

    def __init__(
        self,
        attack_weight=10.0,
        defence_weight=10.0,
    ):
        self.ratings = EloAttackDefence()

        self.team_form = TeamForm()

        self.predictor = AttackDefencePredictor(
            attack_weight=attack_weight,
            defence_weight=defence_weight,
        )

        self.value_detector = ValueDetector()

        self.backtester = Backtester()

    def run(
        self,
        df
    ):
        print(
            "Running Attack/Defence Walk Forward Backtest..."
        )

        df = df.sort_values(
            by="Date"
        )

        for _, match in df.iterrows():
            home = match[
                "HomeTeam"
            ]

            away = match[
                "AwayTeam"
            ]

            prediction = self.predictor.predict(
                home_overall=(
                    self.ratings.get_overall(
                        home
                    )
                ),
                away_overall=(
                    self.ratings.get_overall(
                        away
                    )
                ),
                home_attack=(
                    self.ratings.get_attack(
                        home
                    )
                ),
                away_attack=(
                    self.ratings.get_attack(
                        away
                    )
                ),
                home_defence=(
                    self.ratings.get_defence(
                        home
                    )
                ),
                away_defence=(
                    self.ratings.get_defence(
                        away
                    )
                ),
                form_difference=(
                    self.team_form.get_difference(
                        home,
                        away
                    )
                ),
            )

            home_value = (
                self.value_detector.calculate_edge(
                    prediction[
                        "home_win"
                    ],
                    match[
                        "HomeOdds"
                    ],
                )
            )

            away_value = (
                self.value_detector.calculate_edge(
                    prediction[
                        "away_win"
                    ],
                    match[
                        "AwayOdds"
                    ],
                )
            )

            if self.value_detector.is_value_bet(
                home_value[
                    "edge"
                ]
            ):
                self.backtester.place_bet(
                    probability=prediction[
                        "home_win"
                    ],
                    odds=match[
                        "HomeOdds"
                    ],
                    result=(
                        "WIN"
                        if match["FTHG"] > match["FTAG"]
                        else "LOSS"
                    ),
                    home_team=home,
                    away_team=away,
                    date=match[
                        "Date"
                    ],
                )

            elif self.value_detector.is_value_bet(
                away_value[
                    "edge"
                ]
            ):
                self.backtester.place_bet(
                    probability=prediction[
                        "away_win"
                    ],
                    odds=match[
                        "AwayOdds"
                    ],
                    result=(
                        "WIN"
                        if match["FTAG"] > match["FTHG"]
                        else "LOSS"
                    ),
                    home_team=home,
                    away_team=away,
                    date=match[
                        "Date"
                    ],
                )

            if match["FTHG"] > match["FTAG"]:
                result = "H"

            elif match["FTHG"] < match["FTAG"]:
                result = "A"

            else:
                result = "D"

            self.ratings.update(
                home=home,
                away=away,
                result=result,
                home_goals=match[
                    "FTHG"
                ],
                away_goals=match[
                    "FTAG"
                ],
            )

            self.team_form.update(
                home,
                away,
                result
            )

        self.backtester.report()

        return self.backtester.bets