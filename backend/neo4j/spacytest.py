import spacy
from pdfminer.high_level import extract_text
from pdfminer.layout import LTTextContainer, LTTextLine, LTChar
from pdfreader import SimplePDFViewer
from spacy import displacy
import pdfminer
import pdfreader

if __name__ == '__main__':

    nlp = spacy.load("de_core_news_lg")
    doc = nlp("Die Studierenden haben Grundkenntnisse der (imperativen) Programmierung sowie Kenntnisse der grundlegenden Datenstrukturen und Algorithmen. Spezifischer: "
              "* Studierende sind mit grundlegenden Konzepten von Programmiersprachen vertraut."
              "* Studierende können den Ablauf von Programmen nachvollziehen und selbst kleinere Programme entwickeln"
              "* Studierende können die Komplexität (insbesondere die Laufzeit) von Algorithmen exakt (für einfache Beispiele) und asymptotisch (O-Notation) abschätzen."
              "* Studierende können Beweise zur Korrektheit von Programmen nachvollziehen und einfachere Beweise selbst führen."
              "* Studierende sind mit den Stärken und Schwächen von einfacheren und fortgeschritteneren Sortieralgorithmen vertraut und können mit diesem Wissen die Wahl eines geeigneten Sortieralgorithmus begründen.")
    for token in doc:
        print(token.text, token.lemma_, token.lemma, token.pos_, token.tag_, token.dep_,
              token.shape_, token.is_alpha, token.is_stop, [child for child in token.children])
        print(f"match (v:volltext {{lemma:\"{token.lemma}\"}})-[:`GEHÖRT_ZU`]-(a) return a.name")
    #displacy.serve(doc, style="dep")

    



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