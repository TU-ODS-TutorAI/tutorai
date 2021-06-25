#!/usr/bin/python3

import difflib
import nltk
nltk.download('punkt')

from HanTa import HanoverTagger as ht
from . import alternativeKeys as aK


def keyWordExtraction(question, language):
    words = nltk.word_tokenize(question, language=language)
  
    query_string = ""
    if(language == "german"):
        tagger = ht.HanoverTagger('morphmodel_ger.pgz')
        lemmata = tagger.tag_sent(words,taglevel=1)

        for lemma in lemmata:
            if(lemma[2] == "NN" or lemma[2] == "NE" or lemma[2].startswith("ADJ") or lemma[2].startswith("VV")):
                query_string = query_string + " " + lemma[0].lower()
    else:
        tagger = nltk.pos_tag(words)
        for tag in tagger:
            if(tag[1].startswith("NN") or tag[1].startswith("VB")):
                query_string = query_string + " " + tag[0].lower()
    
    return query_string


def getAnswers(data, question):
    possible_answers = []

    for key, value in data.items():
        all_keys = aK.getAlternativeKeys(key)
        all_keys.append(key)
        for k in all_keys:
            score = calculateScore(k, question)
            answer = (k, value, score)
            possible_answers.append(answer)

    return possible_answers


def calculateScore(key, question):
    seq = difflib.SequenceMatcher(None, key.lower(), question)
    score = seq.ratio()
    
    return score


def getBestAnswer(answers):
    best = max(answers, key=lambda x:x[2])
    
    return best

