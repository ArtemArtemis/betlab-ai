import pandas as pd

from src.models.elo_engine import EloEngine
from src.models.elo_predictor import EloPredictor
from src.betting.value_detector import ValueDetector


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


    detector = ValueDetector()


    odds = 1.50


    value = detector.calculate_edge(
        prediction["home_win"],
        odds
    )


    print("\n===== VALUE ANALYSIS =====")


    print(
        "Model probability:",
        value["model_probability"]
    )


    print(
        "Market probability:",
        value["market_probability"]
    )


    print(
        "Edge:",
        value["edge"]
    )


    if detector.is_value_bet(
        value["edge"]
    ):

        print(
            "SIGNAL: VALUE BET"
        )

    else:

        print(
            "SIGNAL: NO VALUE"
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