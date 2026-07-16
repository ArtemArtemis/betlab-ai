from src.research.experiment import Experiment
from src.research.runner import ResearchRunner

from src.backtesting.elo_form_blend_walk_forward import (
    EloFormBlendWalkForwardBacktester
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

    name="Elo Form Blend",

    model="EloFormBlendWalkForwardBacktester",

    features=[
        "Elo",
        "TeamForm",
        "FormBlend"
    ],

    parameters={

        "form_blend_weight":
            0.2,

        "min_edge":
            MODEL_CONFIG["min_edge"],

        "max_edge":
            MODEL_CONFIG["max_edge"]

    }

)



runner = ResearchRunner(

    experiment,

    EloFormBlendWalkForwardBacktester

)


runner.run(
    seasons
)