import spacy
from py2neo import Graph

password = "TUTORAI"

if __name__ == '__main__':
    neo4j = Graph("bolt://localhost:7687", auth=("neo4j", password))
    nlp = spacy.load("de_core_news_lg")

    for data in neo4j.run("match (m) return m, labels(m)").data():
        for data1 in data["m"]:
            output = nlp(data["m"][data1])
            # print(data["m"]["name"])
            # print(data)
            # print(data["m"])
            # print(data["labels(m)"][0])
            """
            reihen reihen 12381519186764585653 VERB VVFIN cj xxxx True False [unendliche, ,]
            Reihen Reihe 15981145232003321657 NOUN NN cj Xxxxx True False [unendliche, ,, Potenzreihen, ,]
            str_data = str(data["m"])
            str_data_arr = str_data.split(':')
            str_data = str_data_arr[1]
            if str_data[0] == "`":
                str_data_arr = str_data.split("`")
                das_was_du_willst = str_data_arr[1]

            else:
                str_data_arr = str_data.split(' ')
                das_was_du_willst = str_data_arr[0]

            print(das_was_du_willst)
            """

            # print(data["m"])
            for token in output:
                if token.pos_ != "PUNCT" and token.pos_ != "SPACE":
                    print(token.text.lower())
                    if data["labels(m)"][0] != "Modul":
                        for moduleName in neo4j.run(f"match (m:`{data['labels(m)'][0]}` {{name:'{data['m']['name']}'}})--(a:Modul) return a.name").data():
                            neo4j.run(f"merge (t:volltext {{lemma:'{token.lemma}', text:'{token.text.lower()}'}}) "
                                      f"merge(m:Modul {{name:'{moduleName['a.name']}'}}) "
                                      "merge(t)-[rel:GEHÖRT_ZU]->(m)")
                    else:
                        neo4j.run(f"merge (t:volltext {{lemma:'{token.lemma}', text:'{token.text.lower()}'}}) "
                                  f"merge(m:Modul {{name:'{data['m']['name']}'}}) "
                                  "merge(t)-[rel:GEHÖRT_ZU]->(m)")
