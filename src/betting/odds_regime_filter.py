class OddsRegimeFilter:


    def __init__(self):

        self.rules = {

            "3.0-4.0":
                0.10,

            "4.0-5.0":
                0.12,

            "5.0+":
                0.06

        }



    def get_regime(
        self,
        odds
    ):


        if 3.0 <= odds < 4.0:

            return "3.0-4.0"


        if 4.0 <= odds < 5.0:

            return "4.0-5.0"


        if odds >= 5.0:

            return "5.0+"



        return None



    def is_valid(
        self,
        odds,
        edge
    ):


        regime = self.get_regime(
            odds
        )


        if regime is None:

            return False



        return (
            edge
            >=
            self.rules[regime]
        )