import pandas as pd

from src.backtesting.walk_forward import (
    WalkForwardBacktester
)

from src.config.model_config import MODEL_CONFIG

from src.features.football_features import (
    FootballFeatures
)

from src.research.experiment import (
    Experiment
)

from src.research.runner import (
    ResearchRunner
)



SEASONS = {

    "2022/23":
        "data/raw/"
        "premier_league_2022_23.csv",

    "2023/24":
        "data/raw/"
        "premier_league_2023_24.csv",

    "2024/25":
        "data/raw/"
        "premier_league_2024_25.csv",
}



def load_season(
    path
):

    df = pd.read_csv(
        path
    )

    return FootballFeatures(
        df
    ).prepare()



def main():


    MODEL_CONFIG[
        "form_weight"
    ] = 80


    MODEL_CONFIG[
        "min_edge"
    ] = 0.07


    MODEL_CONFIG[
        "max_edge"
    ] = 0.12



    seasons = {

        name:
        load_season(path)

        for name, path
        in SEASONS.items()

    }


    experiment = Experiment(

        name="Baseline Elo",

        model="WalkForwardBacktester",

        features=[
            "Elo",
            "TeamForm"
        ],

        parameters={

            "form_weight":80,

            "min_edge":0.07,

            "max_edge":0.12

        }

    )


    backtester = (
        WalkForwardBacktester()
    )


    runner = ResearchRunner(

        experiment,

        WalkForwardBacktester

    )


    runner.run(
        seasons
    )



if __name__ == "__main__":

    main()