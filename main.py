from src.collectors.football_data import FootballDataCollector


def main():
    collector = FootballDataCollector()

    df = collector.create_sample_dataset()

    print(df)
    print("\nData saved successfully.")


if __name__ == "__main__":
    main()