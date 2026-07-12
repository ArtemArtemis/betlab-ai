from src.research.experiment import Experiment
from src.research.runner import ResearchRunner

from src.backtesting.home_away_filter_walk_forward import (
    HomeAwayFilterWalkForwardBacktester
)

from src.config.model_config import MODEL_CONFIG

from src.features.football_features import FootballFeatures

import pandas as pd



SEASONS = {

    "2022/23":
        "data/raw/premier_league_2022_23.csv",

    "2023/24":
        "data/raw/premier_league_2023_24.csv",

    "2024/25":
        "data/raw/premier_league_2024_25.csv",

}



def load_season(path):

    df = pd.read_csv(path)

    features = FootballFeatures(df)

    return features.prepare()



seasons = {}


for name, path in SEASONS.items():

    seasons[name] = load_season(path)



experiment = Experiment(

    name="Home Away Filter Elo",

    model="HomeAwayFilterWalkForwardBacktester",

    features=[
        "Elo",
        "TeamForm",
        "HomeAwayFilter"
    ],

    parameters={

        "form_weight":
            MODEL_CONFIG["form_weight"],

        "min_edge":
            MODEL_CONFIG["min_edge"],

        "max_edge":
            MODEL_CONFIG["max_edge"],

        "home_away_min_form":
            0.5

    }

)



runner = ResearchRunner(

    experiment,

    HomeAwayFilterWalkForwardBacktester

)


runner.run(
    seasons
)