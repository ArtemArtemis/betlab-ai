from src.research.experiment import Experiment
from src.research.runner import ResearchRunner

from src.backtesting.dynamic_stake_walk_forward import (
    DynamicStakeWalkForwardBacktester
)

from src.features.football_features import FootballFeatures

from src.config.model_config import MODEL_CONFIG

import pandas as pd



SEASONS = {

    "2022/23":
        "data/raw/premier_league_2022_23.csv",

    "2023/24":
        "data/raw/premier_league_2023_24.csv",

    "2024/25":
        "data/raw/premier_league_2024_25.csv"

}



def load(path):

    df = pd.read_csv(path)

    return FootballFeatures(df).prepare()



seasons = {

    name:
    load(path)

    for name, path in SEASONS.items()

}



experiment = Experiment(

    name="Dynamic Stake Management",

    model="DynamicStakeWalkForwardBacktester",

    features=[

        "Elo",

        "TeamForm",

        "DynamicStake"

    ],

    parameters={

        "stake_mode":
            "edge_based",

        "min_edge":
            MODEL_CONFIG["min_edge"],

        "max_edge":
            MODEL_CONFIG["max_edge"]

    }

)



runner = ResearchRunner(

    experiment,

    DynamicStakeWalkForwardBacktester

)


runner.run(
    seasons
)