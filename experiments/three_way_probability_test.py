from src.research.experiment import Experiment
from src.research.runner import ResearchRunner

from src.backtesting.three_way_probability_walk_forward import (
    ThreeWayProbabilityWalkForwardBacktester
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

    name="Three Way Probability Elo",

    model="ThreeWayProbabilityWalkForwardBacktester",

    features=[
        "Elo",
        "ThreeWayProbability"
    ],

    parameters={

        "home_advantage":
            60,

        "draw_probability":
            0.25,

        "min_edge":
            MODEL_CONFIG["min_edge"]

    }

)



runner = ResearchRunner(

    experiment,

    ThreeWayProbabilityWalkForwardBacktester

)


runner.run(
    seasons
)