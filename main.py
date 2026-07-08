import pandas as pd

from src.features.football_features import FootballFeatures
from src.backtesting.walk_forward import WalkForwardBacktester


# 1. Загружаем данные

df = pd.read_csv(
    "data/raw/premier_league.csv"
)


# 2. Создаем признаки

features = FootballFeatures(df)

df = features.prepare()


# 3. Сохраняем

features.save(df)


# 4. Запускаем Walk Forward Backtest

backtester = WalkForwardBacktester()

backtester.run(df)