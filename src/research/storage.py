import json
import os


class ExperimentStorage:


    def __init__(self):

        self.path = (
            "data/research/results"
        )

        os.makedirs(
            self.path,
            exist_ok=True
        )


    def save(
        self,
        name,
        result
    ):

        filename = (
            name
            .lower()
            .replace(" ", "_")
            +
            ".json"
        )


        filepath = os.path.join(
            self.path,
            filename
        )


        with open(
            filepath,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                result,
                file,
                indent=4,
                ensure_ascii=False
            )


        print(
            f"Saved result: {filepath}"
        )


    def load_all(self):

        results = []


        for filename in os.listdir(
            self.path
        ):

            if filename.endswith(".json"):

                filepath = os.path.join(
                    self.path,
                    filename
                )


                with open(
                    filepath,
                    encoding="utf-8"
                ) as file:

                    results.append(
                        json.load(file)
                    )


        return results