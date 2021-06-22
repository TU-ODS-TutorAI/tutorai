from allennlp.predictors.predictor import Predictor
import json


class Parser:
    def __init__(self):
        download = "https://storage.googleapis.com/allennlp-public-models/structured-prediction-srl-bert.2020.12.15" \
                   ".tar.gz "
        self.predictor_model = Predictor.from_path(download)

    def extract(self, input_text):
        tree = self.predictor_model.predict(sentence=input_text)

        with open("output.json", "w") as outfile:
            json.dump(tree['verbs'], outfile)
