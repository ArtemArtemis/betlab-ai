from src.collectors.football_data import FootballDataCollector
from src.validators.data_validator import DataValidator


def main():

    collector = FootballDataCollector()

    df = collector.download_season("2425")

    collector.save_data(df)


    validator = DataValidator(df)

    validator.report()


if __name__ == "__main__":
    main()