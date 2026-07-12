from src.config.model_config import MODEL_CONFIG
from src.backtesting.walk_forward import WalkForwardBacktester


class ParameterOptimizer:


    def __init__(
        self,
        df
    ):

        self.df = df

        self.results = []


    def run(
        self,
        form_weights,
        edge_ranges
    ):

        print(
            "\n===== PARAMETER OPTIMIZATION ====="
        )


        for form_weight in form_weights:


            for min_edge, max_edge in edge_ranges:


                print(
                    f"\nTesting:"
                    f" form_weight={form_weight}"
                    f" edge={min_edge}-{max_edge}"
                )


                MODEL_CONFIG[
                    "form_weight"
                ] = form_weight


                MODEL_CONFIG[
                    "min_edge"
                ] = min_edge


                MODEL_CONFIG[
                    "max_edge"
                ] = max_edge


                backtester = (
                    WalkForwardBacktester()
                )


                bets = backtester.run(
                    self.df
                )


                if len(bets) == 0:

                    continue


                profit = sum(
                    bet["profit"]
                    for bet in bets
                )


                total_stake = sum(
                    bet["stake"]
                    for bet in bets
                )


                roi = (
                    profit
                    /
                    total_stake
                )


                self.results.append(
                    {
                        "form_weight": form_weight,
                        "min_edge": min_edge,
                        "max_edge": max_edge,
                        "bets": len(bets),
                        "profit": round(
                            profit,
                            2
                        ),
                        "roi": round(
                            roi * 100,
                            2
                        )
                    }
                )


        return self.results



    def report(self):

        print(
            "\n===== OPTIMIZATION RESULTS ====="
        )


        sorted_results = sorted(
            self.results,
            key=lambda x: x["roi"],
            reverse=True
        )


        for result in sorted_results[:10]:

            print(
                result
            )