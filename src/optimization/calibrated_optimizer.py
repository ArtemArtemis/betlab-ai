from copy import deepcopy

from src.backtesting.calibrated_walk_forward import (
    CalibratedWalkForwardBacktester,
)
from src.config.model_config import MODEL_CONFIG


class CalibratedOptimizer:

    def __init__(
        self,
        calibrator,
        seasons
    ):

        self.calibrator = calibrator

        self.seasons = seasons

        self.results = []


    def calculate_metrics(
        self,
        bets
    ):

        total_bets = len(
            bets
        )

        if total_bets == 0:

            return {
                "bets": 0,
                "profit": 0,
                "roi": 0,
            }


        profit = sum(
            bet["profit"]
            for bet in bets
        )


        stake = sum(
            bet["stake"]
            for bet in bets
        )


        roi = (
            profit
            /
            stake
            *
            100
        )


        return {
            "bets": total_bets,
            "profit": profit,
            "roi": roi,
        }


    def run_test(
        self,
        min_edge,
        max_edge
    ):

        original_config = deepcopy(
            MODEL_CONFIG
        )


        season_results = []


        try:

            MODEL_CONFIG[
                "min_edge"
            ] = min_edge


            MODEL_CONFIG[
                "max_edge"
            ] = max_edge


            for (
                season_name,
                dataframe
            ) in self.seasons.items():


                backtester = (
                    CalibratedWalkForwardBacktester(
                        self.calibrator
                    )
                )


                bets = backtester.run(
                    dataframe.copy()
                )


                metrics = (
                    self.calculate_metrics(
                        bets
                    )
                )


                season_results.append(
                    {
                        "season": season_name,
                        **metrics
                    }
                )


        finally:

            MODEL_CONFIG.clear()

            MODEL_CONFIG.update(
                original_config
            )


        total_bets = sum(
            result["bets"]
            for result in season_results
        )


        total_profit = sum(
            result["profit"]
            for result in season_results
        )


        total_stake = (
            total_bets
            *
            MODEL_CONFIG["stake"]
        )


        combined_roi = (
            total_profit
            /
            total_stake
            *
            100
            if total_stake > 0
            else 0
        )


        profitable_seasons = sum(
            1
            for result in season_results
            if result["profit"] > 0
        )


        result = {

            "min_edge": min_edge,

            "max_edge": max_edge,

            "total_bets": total_bets,

            "total_profit": total_profit,

            "combined_roi": combined_roi,

            "profitable_seasons": (
                profitable_seasons
            ),

            "season_results": season_results
        }


        self.results.append(
            result
        )


        return result



    def optimize(
        self,
        edge_ranges
    ):


        print(
            "\n===== CALIBRATED OPTIMIZATION ====="
        )


        for (
            min_edge,
            max_edge
        ) in edge_ranges:


            print(
                "\nTesting:"
            )

            print(
                f"{min_edge:.2f}"
                "-"
                f"{max_edge:.2f}"
            )


            result = self.run_test(
                min_edge,
                max_edge
            )


            print(
                f"Bets: "
                f"{result['total_bets']}"
            )

            print(
                f"Profit: "
                f"{result['total_profit']:+.2f}"
            )

            print(
                f"ROI: "
                f"{result['combined_roi']:+.2f}%"
            )

            print(
                "Profitable seasons: "
                f"{result['profitable_seasons']}/2"
            )


        self.results.sort(
            key=lambda x:
            (
                x["combined_roi"],
                x["profitable_seasons"]
            ),
            reverse=True
        )


        return self.results