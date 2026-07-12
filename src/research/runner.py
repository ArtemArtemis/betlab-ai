from src.evaluation.metrics import BettingMetrics
from src.research.report import ExperimentReport
from src.research.storage import ExperimentStorage



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

        self.storage = ExperimentStorage()



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


        total_metrics = {
            "bets":0,
            "profit":0,
            "roi":0
        }


        for (
            season_name,
            dataframe
        ) in seasons.items():


            print(
                f"\nRunning season: {season_name}"
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


            total_metrics["bets"] += (
                metrics["bets"]
            )

            total_metrics["profit"] += (
                metrics["profit"]
            )


        if total_metrics["bets"] > 0:

            total_metrics["roi"] = (

                total_metrics["profit"]

                /

                (
                    total_metrics["bets"]
                    *
                    10
                )

                *

                100
            )


        result = {

            "experiment":
                self.experiment.name,

            "model":
                self.experiment.model,

            "features":
                self.experiment.features,

            "parameters":
                self.experiment.parameters,

            "results":
                total_metrics

        }


        self.storage.save(
            self.experiment.name,
            result
        )


        report.summary()


        return report