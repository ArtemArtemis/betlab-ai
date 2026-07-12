import pandas as pd

from src.features.football_features import FootballFeatures
from src.backtesting.walk_forward import WalkForwardBacktester
from src.analysis.betting_analysis import BettingAnalyzer


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

bets = backtester.run(df)

analyzer = BettingAnalyzer(
    bets
)

analyzer.summary()

analyzer.analyze_edge()