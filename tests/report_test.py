from src.research.report import ExperimentReport


report = ExperimentReport(
    "Baseline Elo"
)


report.add_result(
    "2023/24",
    {
        "bets":117,
        "profit":-142.90,
        "roi":-12.21
    }
)


report.add_result(
    "2024/25",
    {
        "bets":141,
        "profit":159.40,
        "roi":11.30
    }
)


report.summary()