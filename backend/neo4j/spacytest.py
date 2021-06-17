import spacy
from spacy import displacy

if __name__ == '__main__':

    nlp = spacy.load("de_core_news_lg")
    doc = nlp("Quicksort (englisch quick ‚schnell‘ und to sort ‚sortieren‘) ist ein schneller, rekursiver, nicht-stabiler Sortieralgorithmus, der nach dem Prinzip Teile und herrsche arbeitet. Er wurde ca. 1960 von C. Antony R. Hoare in seiner Grundform entwickelt[1] und seitdem von vielen Forschern verbessert. Der Algorithmus hat den Vorteil, dass er über eine sehr kurze innere Schleife verfügt (was die Ausführungsgeschwindigkeit stark erhöht) und dass er, abgesehen von dem für die Rekursion zusätzlichen benötigten Platz auf dem Aufruf-Stack, ohne zusätzlichen Speicherplatz auskommt.")
    for token in doc:
        print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
              token.shape_, token.is_alpha, token.is_stop, [child for child in token.children])
    displacy.serve(doc, style="dep")