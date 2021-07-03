import json
import requests
from transformers import pipeline
import openai
import os


def get_config_file():
    global config

    path_to_config_file = os.path.join(os.path.dirname(__file__), "config.json")
    relative_path_to_config_file = os.path.relpath(path_to_config_file)
    with open(relative_path_to_config_file) as json_config_file:
        config = json.load(json_config_file)


get_config_file()


def get_answer(question: str, context: str) -> str:

    if config["ml_config"]["model"] == "GPT3":
        response = gpt3_question_answerer(question, context)
    else:
        response = bert_question_answerer(question, context)

    print("RESPONSE: " + response)
    return response


def get_answer_with_module_number(question: str, module_number: int) -> str:
    response = get_module_data_from_moses(module_number)

    return get_answer(question, str(response.json()))


def get_module_data_from_moses(module_number):
    try:
        response = requests.get(f"http://tutorai.ddns.net:3000/Moses/{module_number}")
    except requests.exceptions.RequestException as e:
        SystemError(e)
    if response.status_code != 200:
        print(
            f"ERROR when trying to fetch moses module data for module number {module_number}. Status Code: {response.status_code}")
        exit(1)
    return response


def bert_question_answerer(question, context):
    question_answerer = pipeline('question-answering')

    payload = {
        'question': question,
        'context': context
    }
    response = question_answerer(payload)

    if response["score"] < config["ml_config"]["score_toleration"]:
        return config["ml_config"]["default_answer"]
    else:
        return response["answer"]


def gpt3_question_answerer(question, context):
    openai.api_key = config["GPT3_config"]["api_key"]

    question_sequence = "\n\nQ: " + question
    answere_sequence = "\nA: "

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

    return response["choices"][0]["text"]


if __name__ == '__main__':
    get_config_file()
