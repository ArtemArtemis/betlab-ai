from src.research.scoring import ResearchScore


score = ResearchScore()


result = {

    "roi":0.64,

    "bets":258,

    "profitable_seasons":2,

    "total_seasons":3
}


print(
    score.calculate(result)
)