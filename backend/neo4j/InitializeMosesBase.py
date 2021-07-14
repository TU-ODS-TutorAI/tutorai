# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from __future__ import print_function

# ------------- config -------------------
# Cypher to show graph: match (m) return m
# 1 = German | 2 = English
language = 1
# the local neo4j password
password = "TUTORAI"
# read only courses that are taught in specified language
onlyNative = True
# all = read the entire MosesDB
# fac4 = read only faculty 4
# testSet = read only:
#   NativeGerman:
#   40017 40356 40019 20122 40029 40672 40908 40511 40985
#   NativeEnglish:
#   40440 40834 40382 40707 40399 40908 40511 40985
readMode = "testSet"


def translate(data, lang):
    if lang == 1:
        if data["contactPerson"] == "Keine Angabe":
            data["contactPerson"] = data["responsiblePerson"]

        data["german"]["learningOutcomes"] = data["german"]["learningOutcomes"].replace("'", "")
        data["german"]["content"] = data["german"]["content"].replace("'", "")
        data["german"]["teachingAndLearningMethods"] = data["german"]["teachingAndLearningMethods"].replace("'", "")
        data["german"]["registrationProcedures"] = data["german"]["registrationProcedures"].replace("'", "")
        data["german"]["literature"] = data["german"]["literature"].replace("'", "")

        for data1 in data:
            if not data[data1]:
                data[data1] = "Keine Angaben"

            if data1 == "german" or data1 == "english":
                for data2 in data[data1]:
                    if not data[data1][data2]:
                        data[data1][data2] = "Keine Angaben"

    if lang == 2:
        if data["contactPerson"] == "Keine Angabe":
            data["contactPerson"] = data["responsiblePerson"]

        data["english"]["learningOutcomes"] = data["english"]["learningOutcomes"].replace("'", "")
        data["english"]["content"] = data["english"]["content"].replace("'", "")
        data["english"]["teachingAndLearningMethods"] = data["english"]["teachingAndLearningMethods"].replace("'", "")
        data["english"]["registrationProcedures"] = data["english"]["registrationProcedures"].replace("'", "")
        data["english"]["literature"] = data["english"]["literature"].replace("'", "")
        data["english"]["desirablePrerequisites"] = data["english"]["desirablePrerequisites"].replace("'", "")

        if not data["english"]["title"]:
            data["english"]["title"] = data["german"]["title"]

        for data1 in data:
            if not data[data1] or data[data1] == "Keine Angaben":
                data[data1] = "not specified"

            if data1 == "german" or data1 == "english":
                for data2 in data[data1]:
                    if not data[data1][data2] or data[data1][data2] == "Keine Angaben":
                        data[data1][data2] = "not specified"


if __name__ == '__main__':

    from neo4j import GraphDatabase

    uri = "bolt://localhost:7687"
    driver = GraphDatabase.driver(uri, auth=("neo4j", password))


    def write_module(tx, data, lang):
        if lang == 2:
            translate(data, lang)
            f = "merge (m:module {name: '%s'," % (data["english"]["title"]) + \
                "`learning outcomes`: '%s'," % data["english"]["learningOutcomes"] + \
                "content: '%s'," % data["english"]["content"] + \
                "`module number`: '%s'," % str(data["number"]) + \
                "version: '%s'," % data["version"] + \
                "`teaching and learning methods`: '%s'," % data["english"]["teachingAndLearningMethods"] + \
                "`desirable prerequisites`: '%s'," % data["english"]["desirablePrerequisites"] + \
                "`mandatory requirements`: '%s'})" % data["english"]["mandatoryRequirements"] + \
                "merge (g:grading {name: '%s'})" % data["english"]["grading"] + \
                "merge (d:duration {name: '%s'})" % data["english"]["duration"] + \
                "merge (dm:`duration of the module` {name: '%s'})" % data["english"]["durationOfTheModule"] + \
                "merge (ma:`maximum number of participants` {name: '%s'})" % data["english"][
                    "maximumNumberOfParticipants"] + \
                "merge (af:`registration procedures` {name: '%s'})" % data["english"]["registrationProcedures"] + \
                "merge (f:faculty {name: '%s'})" % data["faculty"] + \
                "merge (s:office {name: '%s'})" % data["office"] + \
                "merge (i:institute {name: '%s'})" % data["institute"] + \
                "merge (fa:`area of expertise` {name: '%s'})" % data["areaOfExpertise"] + \
                "merge (v:`responsible person` {name: '%s'})" % data["responsiblePerson"] + \
                "merge (a:`contact person` {name: '%s'," % data["contactPerson"] + \
                "email: '%s'})" % data["email"] + \
                "merge (li:literature {name: '%s'})" % data["english"]["literature"] + \
                "merge (l:credits {name:  '%s'})" % str(data["credits"]) + \
                "merge (p:`type of exam` {name: '%s'})" % data["english"]["typeOfExam"] + \
                "merge (m)-[rela:FACULTY]->(f)" + \
                "merge (m)-[relg:GRADING]->(g)" + \
                "merge (p)-[relpg:GRADING]->(g)" + \
                "merge (p)-[relpdm:DURATION]->(d)" + \
                "merge (m)-[relmdm:MODULE_DURATION]->(dm)" + \
                "merge (m)-[relmma:PARTICIPANTS]->(ma)" + \
                "merge (m)-[relmmf:REGISTRATION]->(af)" + \
                "merge (m)-[relb:OFFICE]->(s)" + \
                "merge (m)-[relc:INSTITUTE]->(i)" + \
                "merge (m)-[reld:AREA]->(fa)" + \
                "merge (m)-[rele:RESPOSIBLE_PERSON]->(v)" + \
                "merge (m)-[relf:CONTACT]->(a)" + \
                "merge (m)-[rell:CREDITS]->(l)" + \
                "merge (m)-[relli:LITERATURE]->(li)" + \
                "merge (m)-[relh:EXAM]->(p)"
            tx.run(f)
        if lang == 1:
            translate(data, lang)
            f = "merge (m:Modul {name: '%s'," % (data["german"]["title"]) + \
                "Lernergebnisse: '%s'," % data["german"]["learningOutcomes"] + \
                "Lehrinhalte: '%s'," % data["german"]["content"] + \
                "Modulnummer: '%s'," % str(data["number"]) + \
                "Version: '%s'," % data["version"] + \
                "Lernmethoden: '%s'," % data["german"]["teachingAndLearningMethods"] + \
                "`Wünschenswerte Voraussetzungen`: '%s'," % data["german"]["desirablePrerequisites"] + \
                "`Verpflichtende Voraussetzungen`: '%s'})" % data["german"]["mandatoryRequirements"] + \
                "merge (g:Benotung {name: '%s'})" % data["german"]["grading"] + \
                "merge (d:Dauer {name: '%s'})" % data["german"]["duration"] + \
                "merge (dm:`Dauer des Moduls` {name: '%s'})" % data["german"]["durationOfTheModule"] + \
                "merge (ma:`Maximale teilnehmende Personen` {name: '%s'})" % data["german"][
                    "maximumNumberOfParticipants"] + \
                "merge (af:Anmeldeformalitäten {name: '%s'})" % data["german"]["registrationProcedures"] + \
                "merge (f:Fakultät {name: '%s'})" % data["faculty"] + \
                "merge (s:Sekretariat {name: '%s'})" % data["office"] + \
                "merge (i:Institut {name: '%s'})" % data["institute"] + \
                "merge (fa:Fachgebiet {name: '%s'})" % data["areaOfExpertise"] + \
                "merge (v:`Verantwortliche Person` {name: '%s'})" % data["responsiblePerson"] + \
                "merge (a:`Ansprechpartner` {name: '%s'," % data["contactPerson"] + \
                "email: '%s'})" % data["email"] + \
                "merge (li:Literatur {name: '%s'})" % data["german"]["literature"] + \
                "merge (l:Leistungspunkte {name:  '%s'})" % str(data["credits"]) + \
                "merge (p:Prüfungsform {name: '%s'})" % data["german"]["typeOfExam"] + \
                "merge (m)-[rela:FAKULTÄT]->(f)" + \
                "merge (m)-[relg:BENOTUNG]->(g)" + \
                "merge (p)-[relpg:BENOTUNG]->(g)" + \
                "merge (p)-[relpdm:DAUER]->(d)" + \
                "merge (m)-[relmdm:MODUL_DAUER]->(dm)" + \
                "merge (m)-[relmma:TEILNEHMER]->(ma)" + \
                "merge (m)-[relmmf:ANMELDUNG]->(af)" + \
                "merge (m)-[relb:SEKRETARIAT]->(s)" + \
                "merge (m)-[relc:INSTITUT]->(i)" + \
                "merge (m)-[reld:FACHGEBIET]->(fa)" + \
                "merge (m)-[rele:VERANTWORTLICHER]->(v)" + \
                "merge (m)-[relf:KONTAKT]->(a)" + \
                "merge (m)-[rell:LEISTUNGSPUNKTE]->(l)" + \
                "merge (m)-[relli:LITERATUR]->(li)" + \
                "merge (m)-[relh:PRÜFUNG]->(p)"
            tx.run(f)


    import json
    from urllib.request import urlopen

    url = "http://localhost:3000/moses/"
    response = urlopen(url)
    data_json = json.loads(response.read())


    def islanguage(datamodule, lang):
        if lang == 1:
            if datamodule["german"]["language"] == "Deutsch" or datamodule["german"]["language"] == "Deutsch/Englisch":
                return True
            else:
                return False
        if lang == 2:
            if datamodule["english"]["language"] == "English" or datamodule["english"]["language"] == "German/English":
                return True
            else:
                return False


    def readall(datamodule):
        if not onlyNative or islanguage(datamodule, language):
            with driver.session() as session:
                session.write_transaction(write_module, datamodule, language)


    def readfac4(datamodule):
        if datamodule["faculty"] == "Fakultät IV" and (not onlyNative or islanguage(datamodule, language)):
            with driver.session() as session:
                session.write_transaction(write_module, datamodule, language)


    def readtestset(datamodule):
        if datamodule["number"] in testSet and (not onlyNative or islanguage(datamodule, language)):
            with driver.session() as session:
                session.write_transaction(write_module, datamodule, language)


    switcher = {
        "all": readall,
        "testSet": readtestset,
        "fac4": readfac4
    }

    testSet = [40017, 40356, 40908, 40019, 20122, 40029, 40672, 40511, 40440, 40985, 40834, 40382, 40707, 40399]
    i = 0
    for number in data_json["modules"]:
        response = urlopen(url + str(number["number"]))
        datamodule = json.loads(response.read())
        if i % 50 == 0:
            print(str(i) + "/" + str(len(data_json["modules"])))
        i = i + 1
        func = switcher.get(readMode, lambda: "invalid read mode")
        func(datamodule)
