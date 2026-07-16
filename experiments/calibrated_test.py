from src.research.experiment import Experiment
from src.research.runner import ResearchRunner

from src.backtesting.calibrated_walk_forward import (
    CalibratedWalkForwardBacktester
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

    name="Baseline Elo Probability Calibration",

    model="CalibratedWalkForwardBacktester",

    features=[
        "Elo",
        "TeamForm",
        "ProbabilityCalibration"
    ],

    parameters={

        "form_weight":
            MODEL_CONFIG["form_weight"],

        "min_edge":
            MODEL_CONFIG["min_edge"],

        "max_edge":
            MODEL_CONFIG["max_edge"],

        "model_weight":
            0.7,

        "market_weight":
            0.3

    }

)



runner = ResearchRunner(

    experiment,

    CalibratedWalkForwardBacktester

)


runner.run(
    seasons
)