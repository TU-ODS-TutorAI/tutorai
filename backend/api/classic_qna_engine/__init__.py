#!/usr/bin/python3

import requests
import numpy as np
from textblob import TextBlob

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
    #print("answer from keys:", best_key_answer)

    if(best_key_answer[2] < 0.6):
        #print("going to values")
        bag = BagWords(language)
        
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

def getIsisAnswer(data, user_question, language):
    bag = BagWords(language)

    for message in data:
        bag.add_sentence(message["message"])

    bag.compute_matrix()
    
    bag.tf_idf()
    
    answer_matrix = bag.similarity(user_question)

    max_idx = np.argmax(answer_matrix)
    answer = data[max_idx]["link"]
    return answer

    
def getAnswer(user_question, module_number):
    if not user_question:
        print("Es wurde keine Frage eingegeben")
        exit(1)
    else:
        text = TextBlob(user_question)
        language = text.detect_language()
        if(language == "de"):
            language = "german"
        elif(language == "en"):
            language = "english"
        else:
            print(f"ERROR: cannot interpret langauge {language} or language not supported")
            return("Language of your question could not be interpreted or is not supported")
        
        #isis_data = iD.importIsisData()
        #print(getIsisAnswer(isis_data, user_question, "german"))

        data = getMosesData(module_number, language)
        return getMosesAnswer(data, user_question, language)
