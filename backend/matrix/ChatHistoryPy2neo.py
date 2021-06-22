import py2neo
import spacy
from py2neo import Graph
from spacy import displacy

password = "TUTORAI"


def write_message(graph, token):
    f = "merge (t:%s" % token.pos_ + \
        "{text:'%s' ," % token.text + \
        "lemma:'%s' })" % token.lemma_
    print(f)
    for child in token.children:
        c = "merge (c:%s" % child.pos_ + \
            "{text:'%s' ," % child.text + \
            "lemma:'%s' })" % child.lemma_ + \
            "merge (t:%s" % token.pos_ + \
            "{text:'%s' ," % token.text + \
            "lemma:'%s' })" % token.lemma_ + \
            "merge (t)-[rel:%s]->(c)" % child.dep_
        graph.run(c)


if __name__ == '__main__':
    neo4j = Graph("bolt://localhost:7687", auth=("neo4j", password))

    message = "Jeder der Abgaben durchführen möchte, muss den Check-In durchführen. " \
              "Hier wird ein persönliches Repository erstellt und die Matrikelnummer hinterlegt."

    nlp = spacy.load("de_core_news_lg")
    doc = nlp(message)
    print(doc)
    for token in doc:
        print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
              token.shape_, token.is_alpha, token.is_stop, [child for child in token.children])
        for child in token.children:
            print(child.text, child.lemma_, child.pos_, child.tag_, child.dep_,
                  child.shape_, child.is_alpha, child.is_stop, [child2 for child2 in child.children])
        write_message(neo4j, token)

    print(neo4j.run("match (m:NOUN) return m.text"))
    # displacy.serve(doc, style="dep")
