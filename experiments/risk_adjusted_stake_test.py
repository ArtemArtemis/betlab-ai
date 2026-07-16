from src.research.experiment import Experiment
from src.research.runner import ResearchRunner

from src.backtesting.risk_adjusted_walk_forward import (
    RiskAdjustedWalkForwardBacktester
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

    name="Risk Adjusted Dynamic Stake",

    model="RiskAdjustedWalkForwardBacktester",

    features=[

        "Elo",

        "TeamForm",

        "RiskAdjustedStake"

    ],

    parameters={

        "base_strategy":
            "Dynamic Stake B",

        "drawdown_control":
            True

    }

)



runner = ResearchRunner(

    experiment,

    RiskAdjustedWalkForwardBacktester

)


runner.run(
    seasons
)