from src.evaluation.metrics import BettingMetrics


bets = [

    {
        "win": True,
        "profit": 10,
        "stake": 10
    },

    {
        "win": False,
        "profit": -10,
        "stake": 10
    }

]


metrics = BettingMetrics()

result = metrics.calculate(
    bets
)


print(result)