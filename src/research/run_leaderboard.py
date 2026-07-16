from src.research.leaderboard_v2 import ResearchLeaderboard


if __name__ == "__main__":

    leaderboard = ResearchLeaderboard()

    leaderboard.load_results()

    leaderboard.show()