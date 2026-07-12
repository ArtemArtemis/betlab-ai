from src.models.team_form import TeamForm
from src.models.home_away_form import HomeAwayForm


class WeightedHomeAwayForm:


    def __init__(
        self,
        adjustment_weight=0.3
    ):

        self.team_form = TeamForm()

        self.home_away_form = HomeAwayForm()

        self.adjustment_weight = (
            adjustment_weight
        )



    def get_difference(
        self,
        home_team,
        away_team
    ):

        overall_difference = (
            self.team_form.get_difference(
                home_team,
                away_team
            )
        )


        home_away_difference = (
            self.home_away_form.get_difference(
                home_team,
                away_team
            )
        )


        return (

            overall_difference

            +

            (
                home_away_difference
                *
                self.adjustment_weight
            )

        )



    def update(
        self,
        home_team,
        away_team,
        result
    ):

        self.team_form.update(
            home_team,
            away_team,
            result
        )


        self.home_away_form.update(
            home_team,
            away_team,
            result
        )