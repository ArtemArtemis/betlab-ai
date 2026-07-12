from src.research.experiment import Experiment
from src.research.runner import ResearchRunner

from src.backtesting.probability_adjusted_walk_forward import (
    ProbabilityAdjustedWalkForwardBacktester
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

    name="Probability Adjusted Draw Risk Elo",

    model="ProbabilityAdjustedWalkForwardBacktester",

    features=[
        "Elo",
        "TeamForm",
        "DrawRisk",
        "ProbabilityAdjustment"
    ],

    parameters={

        "form_weight":
            MODEL_CONFIG["form_weight"],

        "min_edge":
            MODEL_CONFIG["min_edge"],

        "max_edge":
            MODEL_CONFIG["max_edge"],

        "draw_penalty":
            0.05

    }

)



runner = ResearchRunner(

    experiment,

    ProbabilityAdjustedWalkForwardBacktester

)


runner.run(
    seasons
)