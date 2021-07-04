#!/usr/bin/python3

import requests
import json
import copy
import pickle
import numpy as np
from textblob import TextBlob
from sentence_transformers import SentenceTransformer

from . import keyTranslation as kT
from . import keyAnswer as kA
from . import valueAnswer as vA
from .BoW import BagWords

def getMosesData(module_number, language):
    try:
        resp = requests.get(f"http://localhost:3000/Moses/{module_number}")
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    
    if resp.status_code != 200:
        print(f"ERROR when trying to fetch moses module data for module number {module_number}. Status Code: {resp.status_code}")
        exit(1)

    data = resp.json()
    del data["_id"]
    del data["__v"]
    
    if(language == "german"):
        del data["english"]
        german_info = data["german"]
        del data["german"]
        data.update(german_info)
        data = kT.translateKeys(data)
    else:
        del data["german"]
        english_info = data["english"]
        del data["english"]
        data.update(english_info)
   
    data = {k : str(v) for k, v in data.items()}
    data = {k : v.replace("\n", " ") for k, v in data.items()}

    return data


def getMosesAnswer(data, user_question, language):
    query = kA.keyWordExtraction(user_question, language)
    if not query:
        return "Ich habe deine Frage nicht verstanden, bitte ändere sie ein bisschen"

    answers = kA.getAnswers(data, query)
    best_key_answer = kA.getBestAnswer(answers)

    if(best_key_answer[2] < 0.6):
        bag = BagWords(language, 1)
        
        answers = []
        for key, value in data.items():
            answers.append(value)

        for answ in answers:
            bag.add_sentence(answ)

        bag.compute_matrix()

        bag.tf_idf()

        answer_matrix = bag.similarity(user_question)

        sorted_idxs = []
        while np.count_nonzero(answer_matrix) != 0:
            max_idx = np.argmax(answer_matrix)
            sorted_idxs.append(max_idx)
            answer_matrix[max_idx] = 0

        final_answer = ""
        if not sorted_idxs:
            final_answer = "leider konnte ich keine Antwort auf deine Frage finden bitte melde dich bei einem Modulverantwortlichen"
        elif(len(sorted_idxs) == 1):
            final_answer = answers[sorted_idxs[0]]
        else:
            final_answer = vA.getBestAnswer(bag.tokens, answers, sorted_idxs)
        return final_answer
    else:
        return best_key_answer[1]


def getIsisData(module):
    with open(f"../crawling/ISIS/{module}.json") as f:
        data = json.load(f)
    return data


def getTfidfIsisAnswer(module, user_question, language):
    bag = BagWords(language, 2)

    bag.texts = pickle.load(open(f"classic_qna_engine/{module}_tfidf_texts.p", "rb"))

    bag.compute_matrix()

    bag.tf_idf()

    answer_matrix = bag.similarity(user_question)

    return answer_matrix


def getMlIsisAnswer(module, user_question):
    model = SentenceTransformer('T-Systems-onsite/cross-en-de-roberta-sentence-transformer')

    ans_matrix = pickle.load(open(f"classic_qna_engine/{module}_model_vectors.p", "rb"))
    q_matrix = model.encode(user_question)

    res_matrix_mul = np.matmul(ans_matrix, q_matrix)

    return res_matrix_mul


    
def getAnswer(user_question, module_number):
    if not user_question:
        print("Es wurde keine Frage eingegeben")
        exit(1)
    else:
        text = TextBlob(user_question)
        language = text.detect_language()
        if(language == "de"):
            language = "german"
            data = getMosesData(module_number, language)
            moses_answer = getMosesAnswer(data, user_question, language)
            if(module_number == "40017"):
                module = "2021_Einfuehrung_Programmierung"
                isis_data = getIsisData(module)
                data_edit = copy.deepcopy(isis_data)
                
                texts = []
                for message in isis_data["messages"]:
                    if(len(message["text"]) < 1000):
                        texts.append(message)
                data_edit["messages"] = texts

                tfidf_answer_matrix = getTfidfIsisAnswer(module, user_question, language)
                ml_answer_matrix = getMlIsisAnswer(module, user_question)

                max_idx_tfidf = np.argmax(tfidf_answer_matrix)
                tfidf_answer = data_edit["messages"][max_idx_tfidf]["link"]

                max_idx_ml = np.argmax(ml_answer_matrix)
                ml_answer = data_edit["messages"][max_idx_ml]["link"]
                
                answer_message = f"Diese Info von der Moses Kursseite konnte ich im Zusammenhang mit deiner Anfrage finden:\n{moses_answer}.\n\nDiese beiden Beiträge aus dem Isis Forum konnte ich im Zusammenhang mit deiner Anfrage finden:\n{tfidf_answer}\n{ml_answer}"
                return answer_message
            else:
                answer_message = f"Diese Info von der Moses Kursseite konnte ich im Zusammenhang mit deiner Anfrage finden:\n{moses_answer}"
                return answer_message
        elif(language == "en"):
            language = "english"
            data = getMosesData(module_number, language)
            moses_answer = getMosesAnswer(data, user_question, language)
            answer_message = f"This information from the Moses Coursepage was found in connection to your request:\n{moses_answer}"
            return answer_message
        else:
            print(f"ERROR: cannot interpret langauge {language} or language not supported")
            return("Language of your question could not be interpreted or is not supported")
