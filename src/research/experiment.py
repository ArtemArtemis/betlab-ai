class Experiment:

    def __init__(
        self,
        name,
        model,
        features=None,
        parameters=None
    ):

        self.name = name

        self.model = model

        self.features = (
            features
            if features
            else []
        )

        self.parameters = (
            parameters
            if parameters
            else {}
        )


    def describe(self):

        print(
            "\n===== EXPERIMENT ====="
        )

        print(
            f"Name: {self.name}"
        )

        print(
            f"Model: {self.model}"
        )

        print(
            "Features:"
        )

        for feature in self.features:

            print(
                f"- {feature}"
            )


        print(
            "Parameters:"
        )

        for key, value in self.parameters.items():

            print(
                f"{key}: {value}"
            )