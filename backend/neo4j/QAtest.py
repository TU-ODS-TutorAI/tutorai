import codecs
import spacy
from py2neo import Graph
from transformers import pipeline
password = "TUTORAI"

if __name__ == '__main__':
    neo4j = Graph("bolt://localhost:7687", auth=("neo4j", password))
    nlp = spacy.load("de_dep_news_trf")

    question = nlp("Wie funktioniert der Bubble Sort?")

    #key = [0]*1000
    key = []
    for i in range(1000):
        key.append(0)

    for word in question:
        # set suche
        if word.pos_ == "NOUN" or word.pos_ == "VERB" or word.pos_ == "PROPN":
            # for data in neo4j.run(f"match (a:{word.pos_} {{word:'{word.text}'}})-[:text]->(t) return t.data").data():
            #     print(data['t.data'])
            for data in neo4j.run(f"match (k:keyword)<-[:KEYSUB]-(ks:subkeyword {{data:'{word.text}'}}) return ID(k)").data():
                key[data['ID(k)']] += 1
            # data = neo4j.run(f"match (k:subkeyword {{data:'{word.text}'}})-[:KEYSUB]->(t) return ID(t)").data()
            # keycount = neo4j.run(f"match (p)<-[:SET]-(w) where id(p) = {data['ID(t)']} return count(w)").data()[0]['count(w)']
            # if data:
            #     if len(data) == neo4j.run(f"match (p)<-[]-(w) where id(p) = {data[0]['ID(t)']} return count(w)").data()[0]['count(w)']:
            #         print(data[0]['t.data'])
    for i in range(1000):
        if key[i] != 0:
            for data in neo4j.run(
                    f"match (s:set)<-[:SET]-(k:keyword)<-[:KEYSUB]-(ks:subkeyword) where ID(k) = {i} return count(ks), s.data").data():
                if key[i] >= data['count(ks)']:
                    print(data['s.data'])

# qa_pipeline = pipeline(
#     "question-answering",
#     model="deepset/gelectra-large-germanquad",
#     tokenizer="deepset/gelectra-large-germanquad"
# )
#
# f = codecs.open("isis.txt", "r", "utf-8")
# text = f.read()
# f.close()
# result = qa_pipeline({
#     'context': "Lernziele• Kenntnisse- elementarer Datenstrukturen- elementarer Such -und Sortierverfahren• Fähigkeiten- Probleme und Strukturen (wieder) zu erkennen- für ein gegebenes Anwendungsproblem die geeignete Datenstruktur zu wählen- den Aufwand (Komplexität) eines Algorithmus bzw. eines C-Programms abzuschätzen",
#     'question': "Sind elementare Datenstrukturen Teil der Lernziele"
# })
#
#
# print(result)