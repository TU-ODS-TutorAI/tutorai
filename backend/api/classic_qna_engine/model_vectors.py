#!/usr/bin/python3

import json
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('T-Systems-onsite/cross-en-de-roberta-sentence-transformer')

with open(f"../../crawling/ISIS/2021_Einfuehrung_Programmierung.json") as f:
    data = json.load(f)

messages = []
for message in data["messages"]:
    if(len(message["text"]) < 1000):
        messages.append(message["text"])

message_vectors = model.encode(messages)

pickle.dump(message_vectors, open("2021_Einfuehrung_Programmierung_model_vectors.p", "wb"))

