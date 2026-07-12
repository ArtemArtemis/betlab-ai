from src.research.comparison import ExperimentComparison


comparison = ExperimentComparison()


comparison.add(
    "Baseline Elo",
    {
        "bets":258,
        "profit":16.50,
        "roi":0.64
    }
)


comparison.add(
    "Attack Defence Elo",
    {
        "bets":211,
        "profit":-152.40,
        "roi":-7.22
    }
)


comparison.add(
    "Three Way Model",
    {
        "bets":282,
        "profit":-145.40,
        "roi":-5.16
    }
)


comparison.show()