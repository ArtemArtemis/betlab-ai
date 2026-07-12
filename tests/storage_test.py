from src.research.storage import ExperimentStorage


storage = ExperimentStorage()


storage.save(
    "Baseline Elo",
    {
        "bets":258,
        "profit":16.50,
        "roi":0.64,
        "parameters":{
            "form_weight":80,
            "min_edge":0.07,
            "max_edge":0.12
        }
    }
)


results = storage.load_all()


print(results)