#!/usr/bin/python3

import json
import pickle
from BoW import BagWords

bag = BagWords("german", 1)

with open(f"../../crawling/ISIS/2021_Einfuehrung_Programmierung.json") as f:
    data = json.load(f)

texts = []
for message in data["messages"]:
    if(len(message["text"]) < 1000):
        parsed_message = bag.str_2_vec(message["text"])
        texts.append(parsed_message)


pickle.dump(texts, open("2021_Einfuehrung_Programmierung_tfidf_texts.p", "wb"))
