import spacy
from spacy import displacy

if __name__ == '__main__':

    nlp = spacy.load("de_dep_news_trf")
    doc = nlp("Ein Binärbaum T ist eine Struktur, die auf einer endlichen Menge definiert ist. Diese Menge nennt man auch die Knotenmenge des Binärbaums.")
    for token in doc:
        print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
              token.shape_, token.is_alpha, token.is_stop)
    displacy.serve(doc, style="dep")