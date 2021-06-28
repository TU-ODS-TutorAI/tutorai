import flask
import json
from flask import jsonify
from flask_cors import CORS

import machine_learning_qna_engine
import classic_qna_engine

app = flask.Flask(__name__)
cors = CORS(app)
app.config["DEBUG"] = True

with open("config.json") as json_config_file:
    config = json.load(json_config_file)


@app.route("/", methods=["GET"])
def home():
    return "<h1>TutorAI QnA Engine</h1>"


@app.route("/tutorai/machine_learning/<question>/<context>", methods=["GET"])
def machine_learning_question_answering_api(question, context):
    answer = machine_learning_qna_engine.get_answer(str(question), str(context))
    print("ANSWER "+ answer)
    return jsonify(answer=answer)

@app.route("/tutorai/classic/<question>/<module>", methods=["GET"])
def classic_question_answering_api(question, module):
    return jsonify(answer=classic_qna_engine.getAnswer(str(question), module))


if __name__ == '__main__':
    print(config["server_config"])
    app.run(host=config["server_config"]["host"], port=config["server_config"]["port"])
