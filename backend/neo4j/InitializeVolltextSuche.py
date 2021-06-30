import spacy
from py2neo import Graph

password = "TUTORAI"

if __name__ == '__main__':
    neo4j = Graph("bolt://localhost:7687", auth=("neo4j", password))
    nlp = spacy.load("de_core_news_lg")

    for data in neo4j.run("match (m) return m, labels(m)").data():
        for data1 in data["m"]:
            output = nlp(data["m"][data1])
            for token in output:
                if token.pos_ != "PUNCT" and token.pos_ != "SPACE":
                    if data["labels(m)"][0] != "Modul":
                        for moduleName in neo4j.run(f"match (m:`{data['labels(m)'][0]}` {{name:'{data['m']['name']}'}})--(a:Modul) return a.name").data():
                            neo4j.run(f"merge (t:volltext {{lemma:'{token.lemma}', text:'{token.text.lower()}'}}) "
                                      f"merge(m:Modul {{name:'{moduleName['a.name']}'}}) "
                                      "merge(t)-[rel:GEHÖRT_ZU]->(m)")
                    else:
                        neo4j.run(f"merge (t:volltext {{lemma:'{token.lemma}', text:'{token.text.lower()}'}}) "
                                  f"merge(m:Modul {{name:'{data['m']['name']}'}}) "
                                  "merge(t)-[rel:GEHÖRT_ZU]->(m)")
