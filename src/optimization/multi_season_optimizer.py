from copy import deepcopy
from statistics import mean, pstdev

from src.backtesting.walk_forward import WalkForwardBacktester
from src.config.model_config import MODEL_CONFIG


class MultiSeasonOptimizer:
    """
    Подбирает параметры модели одновременно на нескольких сезонах.

    Математика прогнозной модели и бэктеста не изменяется.
    Меняется только критерий выбора параметров.

    Основной критерий:
        stability_score = average_roi - roi_std

    Чем выше средний ROI и меньше разброс между сезонами,
    тем выше итоговый score.
    """

    def __init__(self, seasons):
        """
        Parameters
        ----------
        seasons : dict
            Словарь формата:

            {
                "2023/24": dataframe_2023_24,
                "2024/25": dataframe_2024_25,
            }
        """

        if not seasons:
            raise ValueError(
                "MultiSeasonOptimizer получил пустой список сезонов."
            )

        self.seasons = seasons
        self.results = []

    @staticmethod
    def calculate_season_result(bets):
        """
        Рассчитывает статистику одного сезона.
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

    def test_parameters(
        self,
        form_weight,
        min_edge,
        max_edge,
    ):
        """
        Запускает одинаковый набор параметров
        на всех переданных сезонах.
        """

        season_results = {}

        for season_name, dataframe in self.seasons.items():
            backtester = WalkForwardBacktester()

            bets = backtester.run(
                dataframe.copy()
            )

            season_result = (
                self.calculate_season_result(bets)
            )

            season_results[season_name] = season_result

        roi_values = [
            result["roi"]
            for result in season_results.values()
        ]

        average_roi = mean(roi_values)

        roi_std = (
            pstdev(roi_values)
            if len(roi_values) > 1
            else 0.0
        )

        stability_score = average_roi - roi_std

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
            total_profit / total_stake * 100
            if total_stake > 0
            else 0.0
        )

        profitable_seasons = sum(
            1
            for result in season_results.values()
            if result["profit"] > 0
        )

        return {
            "form_weight": form_weight,
            "min_edge": min_edge,
            "max_edge": max_edge,
            "season_results": season_results,
            "total_bets": total_bets,
            "total_wins": total_wins,
            "total_profit": round(total_profit, 2),
            "combined_roi": round(combined_roi, 2),
            "average_roi": round(average_roi, 2),
            "roi_std": round(roi_std, 2),
            "stability_score": round(
                stability_score,
                2,
            ),
            "profitable_seasons": profitable_seasons,
            "seasons_count": len(season_results),
        }

    def run(
        self,
        form_weights,
        edge_ranges,
    ):
        """
        Перебирает все комбинации параметров.
        """

        print(
            "\n===== MULTI SEASON PARAMETER OPTIMIZATION ====="
        )

        self.results = []

        original_config = deepcopy(MODEL_CONFIG)

        try:
            for form_weight in form_weights:
                for min_edge, max_edge in edge_ranges:
                    if min_edge >= max_edge:
                        print(
                            "\nSkipped invalid edge range: "
                            f"{min_edge}-{max_edge}"
                        )
                        continue

                    print(
                        "\n========================================"
                    )
                    print(
                        "Testing parameters:"
                    )
                    print(
                        f"form_weight = {form_weight}"
                    )
                    print(
                        f"edge range = "
                        f"{min_edge:.2f}-{max_edge:.2f}"
                    )
                    print(
                        "========================================"
                    )

                    MODEL_CONFIG["form_weight"] = (
                        form_weight
                    )
                    MODEL_CONFIG["min_edge"] = min_edge
                    MODEL_CONFIG["max_edge"] = max_edge

                    result = self.test_parameters(
                        form_weight=form_weight,
                        min_edge=min_edge,
                        max_edge=max_edge,
                    )

                    self.results.append(result)

                    print(
                        "\nParameter result:"
                    )

                    for (
                        season_name,
                        season_result,
                    ) in result[
                        "season_results"
                    ].items():
                        print(
                            f"{season_name}: "
                            f"Bets={season_result['bets']} | "
                            f"Profit="
                            f"{season_result['profit']:+.2f} | "
                            f"ROI="
                            f"{season_result['roi']:+.2f}%"
                        )

                    print(
                        f"Average ROI: "
                        f"{result['average_roi']:+.2f}%"
                    )
                    print(
                        f"ROI Std Dev: "
                        f"{result['roi_std']:.2f}%"
                    )
                    print(
                        f"Stability Score: "
                        f"{result['stability_score']:+.2f}"
                    )

        finally:
            MODEL_CONFIG.clear()
            MODEL_CONFIG.update(original_config)

        return self.results

    def report(self, top_n=10):
        """
        Выводит лучшие комбинации по stability_score.
        """

        if not self.results:
            print(
                "\nNo optimization results available."
            )
            return

        sorted_results = sorted(
            self.results,
            key=lambda result: (
                result["stability_score"],
                result["combined_roi"],
                result["total_bets"],
            ),
            reverse=True,
        )

        print(
            "\n\n===== MULTI SEASON OPTIMIZATION RESULTS ====="
        )

        for position, result in enumerate(
            sorted_results[:top_n],
            start=1,
        ):
            print(
                "\n----------------------------------------"
            )
            print(
                f"Position: {position}"
            )
            print(
                f"form_weight: "
                f"{result['form_weight']}"
            )
            print(
                f"edge: "
                f"{result['min_edge']:.2f}"
                f"-{result['max_edge']:.2f}"
            )

            for (
                season_name,
                season_result,
            ) in result["season_results"].items():
                print(
                    f"{season_name}: "
                    f"Bets={season_result['bets']} | "
                    f"Wins={season_result['wins']} | "
                    f"Profit="
                    f"{season_result['profit']:+.2f} | "
                    f"ROI="
                    f"{season_result['roi']:+.2f}%"
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
                f"Average ROI: "
                f"{result['average_roi']:+.2f}%"
            )
            print(
                f"ROI Std Dev: "
                f"{result['roi_std']:.2f}%"
            )
            print(
                f"Stability Score: "
                f"{result['stability_score']:+.2f}"
            )
            print(
                "Profitable seasons: "
                f"{result['profitable_seasons']}"
                f"/{result['seasons_count']}"
            )

        best_result = sorted_results[0]

        print(
            "\n\n===== BEST STABLE PARAMETERS ====="
        )
        print(
            f"form_weight = "
            f"{best_result['form_weight']}"
        )
        print(
            f"min_edge = "
            f"{best_result['min_edge']:.2f}"
        )
        print(
            f"max_edge = "
            f"{best_result['max_edge']:.2f}"
        )
        print(
            f"Combined ROI = "
            f"{best_result['combined_roi']:+.2f}%"
        )
        print(
            f"Average ROI = "
            f"{best_result['average_roi']:+.2f}%"
        )
        print(
            f"ROI Std Dev = "
            f"{best_result['roi_std']:.2f}%"
        )
        print(
            f"Stability Score = "
            f"{best_result['stability_score']:+.2f}"
        )