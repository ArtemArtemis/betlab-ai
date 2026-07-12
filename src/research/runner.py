from src.evaluation.metrics import BettingMetrics
from src.research.report import ExperimentReport


class ResearchRunner:


    def __init__(
        self,
        experiment,
        backtester_factory
    ):

        self.experiment = experiment

        self.backtester_factory = (
            backtester_factory
        )

        self.metrics = BettingMetrics()



    def run(
        self,
        seasons
    ):

        print(
            "\n===== RESEARCH RUNNER ====="
        )


        self.experiment.describe()


        report = ExperimentReport(
            self.experiment.name
        )


        for (
            season_name,
            dataframe
        ) in seasons.items():


            print(
                f"\nRunning season: "
                f"{season_name}"
            )


            backtester = (
                self.backtester_factory()
            )


            bets = backtester.run(
                dataframe.copy()
            )


            metrics = self.metrics.calculate(
                bets
            )


            report.add_result(
                season_name,
                metrics
            )


        report.summary()


        return report