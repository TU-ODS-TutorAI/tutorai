import spacy
from pdfminer.high_level import extract_text
from pdfminer.layout import LTTextContainer, LTTextLine, LTChar
from pdfreader import SimplePDFViewer
from py2neo import Graph
from spacy import displacy
import pdfminer
import pdfreader

NEO4JPASSWORD = "TUTORAI"


neo4j = Graph("bolt://localhost:7687", auth=("neo4j", NEO4JPASSWORD))

if __name__ == '__main__':

    nlp = spacy.load("de_core_news_lg")
    s2v = nlp.add_pipe("sense2vec")
    chato = [
        "hallo",
        "Wann ist die Klausur?",
        "Ist der C Kurs Pflicht",
        "Ich habe alle Hausaufgaben bis auf die 7. im C Kurs bestanden und wollte fragen ob ich den C Kurs nun bestanden habe oder nicht, da die 7. Aufgabe 2 Teile hat.",
        "Hat jemand die Aufgaben am Anfang gescreenshotet oder Aufgenommen?",
        "Wie viele Punkte muss man erreichen zu bestehen?",
        "Viel Erfolg :))"
    ]
    responseo = [
        "Hey wie gehts",
        "Morgen",
        "Der C-Kurs is grundvorraussetzung für die Teilnahme an der Prüfung",
        "Ja, hast du. Es zählt nur blattweise, nicht die einzelnen Aufgabenteile. (Ich hatte letztes Jahr genauso viele Aufgaben erfolgreich gelöst und bei mir wurde das Kriterium in QISPOS eingetragen.)",
        "ne, war ja vErbOteN",
        "Du brauchst 50%",
        "Euch auch 😀"
    ]
    #displacy.serve(doc, style="dep")

    for i in range(7):
        chatnlp = nlp(chato[i])
        responsenlp = nlp(responseo[i])
        neo4j.run(f"merge (c:chat {{text:'{chatnlp.text}'}})-[:RESPONSE]->(r:response {{text:'{responsenlp.text}'}})")
    
    string = "Muss ich den c-kurs machen"

    stringnlp = nlp(string)
    best = 0
    responsebest = "Not found"
    for query in neo4j.run("match (c:chat) return c.text").data():
        querynlp = nlp(query['c.text'])
        tmp = stringnlp.similarity(querynlp)
        print(tmp)
        print(best)
        if tmp > best:
            print ("got a winner")
            for response in neo4j.run(f"match (c:chat {{text:'{querynlp.text}'}})-[:RESPONSE]->(r) return r.text").data():
                responsebest = response['r.text']
                best = tmp


    print(responsebest)


    # comp1 = nlp("Studierende können Beweise zur Korrektheit von Programmen nachvollziehen und einfachere Beweise selbst führen.")
    # comp2 = nlp("Etwas zu einfachen beweisen")
    # print (comp1.similarity(comp2))


    # text = extract_text(r'C:\Users\Reste\Downloads\introprog-ws2021-v05-baeume.pdf')
    # print(text)
    # for page_layout in text:
    #     for element in page_layout:
    #         if isinstance(element, LTChar):
    #             print(element)

    # fd = open(r'C:\Users\Reste\Downloads\introprog-ws2021-v05-baeume.pdf',"rb")
    # viewer = SimplePDFViewer(fd)
    # for canvas in viewer:
    #     page_images = canvas.images
    #     page_forms = canvas.forms
    #     page_text = canvas.text_content
    #     page_inline_images = canvas.inline_images
    #     page_strings = canvas.strings