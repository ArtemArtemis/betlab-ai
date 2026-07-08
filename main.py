import pandas as pd

from src.models.elo_engine import EloEngine
from src.models.elo_predictor import EloPredictor


def main():

    df = pd.read_csv(
        "data/processed/premier_league_features.csv"
    )


    engine = EloEngine()

    engine.process_matches(df)

    engine.print_ratings()

    engine.save_ratings()


    predictor = EloPredictor()


    ratings = engine.elo.ratings


    home = "Liverpool"
    away = "Southampton"


    prediction = predictor.predict(
        ratings[home],
        ratings[away]
    )


    print("\n===== MATCH PREDICTION =====")

    print(
        home,
        prediction["home_win"]
    )

    print(
        away,
        prediction["away_win"]
    )


if __name__ == "__main__":
    main()