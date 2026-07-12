from src.research.experiment import Experiment
from src.research.runner import ResearchRunner


experiment = Experiment(
    name="Baseline Elo",
    model="EloPredictor",
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


runner = ResearchRunner(
    experiment
)

runner.run()