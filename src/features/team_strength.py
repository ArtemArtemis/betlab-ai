from collections import defaultdict, deque



class TeamStrength:


    def __init__(
        self,
        window=10
    ):

        self.window = window


        self.home_stats = defaultdict(
            lambda: deque(
                maxlen=self.window
            )
        )


        self.away_stats = defaultdict(
            lambda: deque(
                maxlen=self.window
            )
        )



    def update(

        self,

        home_team,

        away_team,

        home_goals,

        away_goals

    ):


        self.home_stats[
            home_team
        ].append(

            {

                "scored":
                    home_goals,

                "conceded":
                    away_goals

            }

        )


        self.away_stats[
            away_team
        ].append(

            {

                "scored":
                    away_goals,

                "conceded":
                    home_goals

            }

        )



    def _average(

        self,

        data,

        key

    ):


        if not data:

            return 0


        return sum(

            item[key]
            for item in data

        ) / len(data)



    def get_home_attack(

        self,

        team

    ):


        return self._average(

            self.home_stats[team],

            "scored"

        )



    def get_home_defense(

        self,

        team

    ):


        return self._average(

            self.home_stats[team],

            "conceded"

        )



    def get_away_attack(

        self,

        team

    ):


        return self._average(

            self.away_stats[team],

            "scored"

        )



    def get_away_defense(

        self,

        team

    ):


        return self._average(

            self.away_stats[team],

            "conceded"

        )



    def get_strength_difference(

        self,

        home_team,

        away_team

    ):


        home_attack = (

            self.get_home_attack(
                home_team
            )

        )


        away_defense = (

            self.get_away_defense(
                away_team
            )

        )


        away_attack = (

            self.get_away_attack(
                away_team
            )

        )


        home_defense = (

            self.get_home_defense(
                home_team
            )

        )


        return (

            (
                home_attack
                -
                away_defense
            )

            -

            (
                away_attack
                -
                home_defense
            )

        )