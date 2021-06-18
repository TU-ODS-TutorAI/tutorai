import json
from transformers import pipeline
import openai
import os

DEFAULT_ANSWER = "Sorry, I´m not sure"
SCORE_TOLERATION = 0.05


def get_config_file():
    global config

    path_to_config_file = os.path.join(os.path.dirname(__file__), "config.json")
    relative_path_to_config_file = os.path.relpath(path_to_config_file)
    with open(relative_path_to_config_file) as json_config_file:
        config = json.load(json_config_file)
        print("Halllooooo:  ")
        print(config)


get_config_file()


def get_answer(question: str, context: str) -> str:

    if config["ml_config"]["model"] == "GPT3":
        response = gpt3_question_answerer(question, context)
    else:
        response = bert_question_answerer(question, context)

    print("RESPONSE: " + response)
    return response


def bert_question_answerer(question, context):
    question_answerer = pipeline('question-answering')

    payload = {
        'question': question,
        'context': context
    }
    response = question_answerer(payload)

    if response["score"] < config["ml_config"]["score_toleration"]:
        return DEFAULT_ANSWER
    else:
        return response["answer"]


def gpt3_question_answerer(question, context):
    openai.api_key = config["GPT3_config"]["api_key"]

    question_sequence = "\n\nQ: " + question
    answere_sequence = "\nA: "

    print(context + question_sequence + answere_sequence)
    response = openai.Completion.create(
        engine="davinci",
        prompt=context + question_sequence + answere_sequence,
        max_tokens=config["GPT3_config"]["max_tokens"],
        temperature=0,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["\n"]
    )
    print(response["choices"][0]["text"])

    return response["choices"][0]["text"]


if __name__ == '__main__':
    get_config_file()
