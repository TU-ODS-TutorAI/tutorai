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
                if not data["m"]["Modulnummer"]:
                    for moduleName in neo4j.run("match (m:`%s` {name:'%s'})--(a:Modul) return a.name"
                                                % (data["labels(m)"][0], data["m"]["name"])).data():
                        # print(moduleName["a.name"])
                        neo4j.run("merge (t:volltext {lemma:'%s'}) "
                                  "merge(m:Modul {name:'%s'}) "
                                  "merge(t)-[rel:GEHÖRT_ZU]->(m)" % (token.lemma,moduleName["a.name"]))
                else:
                    neo4j.run("merge (t:volltext {lemma:'%s'}) "
                              "merge(m:Modul {name:'%s'}) "
                              "merge(t)-[rel:GEHÖRT_ZU]->(m)" % (token.lemma, data["m"]["name"]))
