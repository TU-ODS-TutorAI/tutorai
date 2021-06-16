# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from __future__ import print_function



def translate(data):
    if data["contactPerson"] == "Keine Angabe":
        data["contactPerson"] = data["responsiblePerson"]
    # switcher = {
    #     "No exam": "Keine Prüfung",
    #     "Homework": "Hausarbeit",
    #     "Presentation": "Referat",
    #     "Written exam": "Schriftliche Prüfung",
    #     "Portfolio examination": "Portfolioprüfung",
    #     "Oral exam": "Mündliche Prüfung"
    # }
    # data["typeOfExam"] = switcher.get(data["typeOfExam"], data["typeOfExam"])
    data["german"]["learningOutcomes"] = data["german"]["learningOutcomes"].replace("'", "")
    data["german"]["content"] = data["german"]["content"].replace("'", "")
    data["german"]["teachingAndLearningMethods"] = data["german"]["teachingAndLearningMethods"].replace("'", "")
    data["german"]["registrationProcedures"] = data["german"]["registrationProcedures"].replace("'", "")
    data["german"]["literature"] = data["german"]["literature"].replace("'", "")
    #todo: leere einträge anpassen
    # for item in data:
    #     # now song is a dictionary
    #     for attribute, value in item.items():
    #         if str(value) == '':
    #             item[attribute] = 'Keine Angaben'

if __name__ == '__main__':

    from neo4j import GraphDatabase

    uri = "bolt://localhost:7687"
    driver = GraphDatabase.driver(uri, auth=("neo4j", "TUTORAI"))

    # currently only german
    def write_module(tx, data, language):
        if language == 2:
            tx.run('merge (m:module {name: "' + data["english"]["title"] + '",' +
                   '`learning Outcomes`: "' + data["english"]["learningOutcomes"] + '",' +
                   'content: "' + data["english"]["content"] + '",' +
                   'modulenummer: "' + str(data["number"]) + '",' +
                   'version: "' + str(data["version"]) + '",' +
                   'website: "' + data["website"] + '"})' +
                   'merge (f:faculty {name: "' + data["faculty"] + '"})' +
                   'merge (s:office {name: "' + data["office"] + '"})' +
                   'merge (i:institute {name: "' + data["institute"] + '"})' +
                   'merge (fa:`area of expertise` {name: "' + data["areaOfExpertise"] + '"})' +
                   'merge (v:`responsible person` {name: "' + data["responsiblePerson"] + '"})' +
                   'merge (a:`contact person` {name: "' + data["contactPerson"] + '",' +
                   'email:"' + data["email"] + '"})' +
                   'merge (l:credits {name: "' + str(data["credits"]) + '"})' +
                   'merge (p:`type of exam` {name: "' + data["typeOfExam"] + '"})' +
                   'merge (m)-[rela:IST_TEIL_VON]->(f)' +
                   'merge (m)-[relb:IST_TEIL_VON]->(s)' +
                   'merge (m)-[relc:IST_TEIL_VON]->(i)' +
                   'merge (m)-[reld:IST_TEIL_VON]->(fa)' +
                   'merge (m)-[rele:WIRD_BETREUT_VON]->(v)' +
                   'merge (m)-[relf:HAT_KONTAKT]->(a)' +
                   'merge (m)-[relg:HAT_LP]->(l)' +
                   'merge (m)-[relh:PUEFUNG_IST]->(p)')
        if language == 1:
            translate(data)
            #merge (m:Modul { name: 'Title' , Lernergebnisse: 'Lernergebnis'}) merge ---
            #todo type of portfolio
            f = "merge (m:Modul {name: '%s'," % (data["german"]["title"]) + \
                "Lernergebnisse: '%s'," % data["german"]["learningOutcomes"] + \
                "Lehrinhalte: '%s'," % data["german"]["content"] + \
                "Modulnummer: '%s'," % str(data["number"]) + \
                "Version: '%s'," % data["version"] + \
                "Lernmethoden: '%s'," % data["german"]["teachingAndLearningMethods"] + \
                "`Wünschenswerte Voraussetzungen`: '%s'," % data["german"]["teachingAndLearningMethods"] + \
                "`Verpflichtende Voraussetzungen`: '%s'})" % data["german"]["teachingAndLearningMethods"] + \
                "merge (g:Benotung {name: '%s'})" % data["german"]["grading"] + \
                "merge (d:Dauer {name: '%s'})" % data["german"]["duration"] + \
                "merge (dm:`Dauer des Moduls` {name: '%s'})" % data["german"]["durationOfTheModule"] + \
                "merge (ma:`Maximale teilnehmende Personen` {name: '%s'})" % data["german"]["maximumNumberOfParticipants"] + \
                "merge (af:Anmeldeformalitäten {name: '%s'})" % data["german"]["registrationProcedures"] + \
                "merge (f:Fakultät {name: '%s'})" % data["faculty"] + \
                "merge (s:Sekretariat {name: '%s'})" % data["office"] +\
                "merge (i:Institut {name: '%s'})" % data["institute"] +\
                "merge (fa:Fachgebiet {name: '%s'})" % data["areaOfExpertise"] +\
                "merge (v:`Verantwortliche Person` {name: '%s'})" % data["responsiblePerson"] +\
                "merge (a:`Ansprechpartner` {name: '%s'," % data["contactPerson"] + \
                "email: '%s'})" % data["email"] +\
                "merge (li:Literatur {name: '%s'})" % data["german"]["literature"] + \
                "merge (l:Leistungspunkte {name:  '%s'})" % str(data["credits"]) +\
                "merge (p:Prüfungsform {name: '%s'})" % data["german"]["typeOfExam"] +\
                "merge (m)-[rela:IST_TEIL_VON]->(f)" + \
                "merge (m)-[relg:HAT_BENOTUNG]->(g)" + \
                "merge (p)-[relpg:HAT_BENOTUNG]->(g)" + \
                "merge (p)-[relpdm:HAT_DAUER]->(d)" + \
                "merge (m)-[relmdm:HAT_DAUER]->(dm)" + \
                "merge (m)-[relmma:HAT_TEILNEHMER]->(ma)" + \
                "merge (m)-[relmmf:HAT_ANMELDUNG]->(af)" + \
                "merge (m)-[relb:IST_TEIL_VON]->(s)" + \
                "merge (m)-[relc:IST_TEIL_VON]->(i)" + \
                "merge (m)-[reld:IST_TEIL_VON]->(fa)" + \
                "merge (m)-[rele:WIRD_BETREUT_VON]->(v)" + \
                "merge (m)-[relf:HAT_KONTAKT]->(a)" + \
                "merge (m)-[rell:HAT_LP]->(l)" + \
                "merge (m)-[relli:HAT_LITERATUR]->(li)" + \
                "merge (m)-[relh:PRUEFUNG_IST]->(p)"

            #print(f)
            tx.run(f)


    import json
    from urllib.request import urlopen

    url = "http://localhost:3000/moses/"
    response = urlopen(url)
    data_json = json.loads(response.read())

    i = 0
    for number in data_json["modules"]:
        i = i + 1
        if i >= 1900:
            response = urlopen(url + str(number["number"]))
            datamodule = json.loads(response.read())
            print(i)
            if (datamodule["german"]["language"] == "Deutsch" and datamodule["faculty"] == "Fakultät IV"):
                with driver.session() as session:
                    session.write_transaction(write_module, datamodule, 1)