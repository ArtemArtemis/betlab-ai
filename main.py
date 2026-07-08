import pandas as pd

from src.backtesting.walk_forward import WalkForwardBacktester


def main():

    df = pd.read_csv(
        "data/raw/premier_league.csv"
    )


    backtester = WalkForwardBacktester()


    backtester.run(df)


if __name__ == "__main__":
    main()