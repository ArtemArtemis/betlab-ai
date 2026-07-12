from src.evaluation.metrics import BettingMetrics
from src.research.report import ExperimentReport
from src.research.storage import ExperimentStorage
from src.research.scoring import ResearchScore



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

        self.scorer = ResearchScore()



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
            "roi":0,
            "profitable_seasons":0,
            "total_seasons":len(seasons)
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


            if metrics["profit"] > 0:

                total_metrics[
                    "profitable_seasons"
                ] += 1


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


            total_metrics[
                "research_score"
            ] = self.scorer.calculate(
                total_metrics
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