import codecs

import spacy
from py2neo import Graph

password = "TUTORAI"


def neo4jmake(textdata, worddata, relation, merge):
    neo4j.run(
        f"merge (m:{merge} {{data:'{textdata.text}'}}) "
        f"merge (n:{worddata.pos_} {{data:'{worddata.text.lower()}'}}) "
        f"merge (n)-[r:{relation}]->(m)"
    )


def neo4jchild(textdatap, textdatac, worddata):
    neo4j.run(
        f"merge (c:child {{data:'{textdatac.text}'}}) "
        f"merge (p:parent {{data:'{textdatap.text}'}}) "
        f"merge (m:{worddata.pos_} {{data:'{worddata.text.lower()}'}}) "
        f"merge (m)-[rc:CHILD]->(c)"
        f"merge (m)-[rp:PARENT]->(p)"
    )


if __name__ == '__main__':
    neo4j = Graph("bolt://localhost:7687", auth=("neo4j", password))
    nlp = spacy.load("de_dep_news_trf")

    f = codecs.open("isis.txt", "r", "utf-8")
    file = f.read()
    f.close()
    file = file.split("--!--")

    for i in range(len(file)):
        file[i] = file[i].strip()
    # for text in file:
    #     for word in text[1:4]:
    #         if word.pos_ == "NOUN" or word.pos_ == "VERB" or word.pos_ == "PROPN":
    #             print(word.text, word.lemma_)
    for text in file:
        if text[0:5] == "--S--":
            text = text[5:]
            text = text.split("--D--")

            for i in range(len(text)):
                text[i] = text[i].strip()
            text[0] = text[0].split(",")

            for word in text[0]:
                neo4j.run(
                    f"merge (k:keyword {{data:'{word.lower()}'}}) "
                    f"merge (s:set {{data:'{text[1]}'}}) "
                    f"merge (k)-[r:SET]->(s)"
                )

        elif text[0:5] == "--P--":
            text = text[5:]
            text = text.split("--C--")

            for i in range(len(text)):
                text[i] = nlp(text[i].strip())

            for word in text[0]:
                if word.pos_ == "NOUN" or word.pos_ == "VERB" or word.pos_ == "PROPN":
                    neo4jmake(text[0], word, "PARENT", "parent")

            for i in range(1, len(text)):
                for word in text[i]:
                    if word.pos_ == "NOUN" or word.pos_ == "VERB" or word.pos_ == "PROPN":
                        neo4jchild(text[0], text[i], word)
                neo4j.run(
                    f"merge (t:child {{data:'{text[i].text}'}}) "
                    f"merge (p:parent {{data:'{text[0].text}'}}) "
                    f"merge (p)-[r:SUB]->(t)"
                )
        else:
            text = nlp(text)
            for word in text:
                if word.pos_ == "NOUN" or word.pos_ == "VERB" or word.pos_ == "PROPN":
                    neo4jmake(text, word, "TEXT", "text")

    for keyword in neo4j.run("match (k:keyword) return k.data"):
        keysplit = keyword['k.data'].strip().split(" ")
        for key in keysplit:
            neo4j.run(
                f"merge (k:keyword {{data:'{keyword['k.data']}'}})"
                f"merge (s:subkeyword {{data:'{key}'}})"
                f"merge (s)-[r:KEYSUB]->(k)"
            )
            # for word in text:
            #     print(word.lemma_)
            #     if word.pos_ == "NOUN":
            #         neo4j.run(
            #             f"merge (t:data {{text:'{text.text}'}}) merge (n:noun {{word:'{word.text}'}}) merge (n)-[r:DATA]->(t)")
            #     if word.pos_ == "VERB":
            #         neo4j.run(
            #             f"merge (t:data {{text:'{text.text}'}}) merge (v:verb {{word:'{word.text}'}}) merge (v)-[r:DATA]->(t)")