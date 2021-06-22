import json
from os import supports_effective_ids
import re
import math
import numpy as np
import nltk
from HanTa import HanoverTagger as ht
import spacy

def score(chars, time):
    chars_sum = chars_for_score(chars)

    exp = time/(1000*60*60*24)
    if exp < 1:                         #priorisiert nachrichten jünger als einen tag
        exp = -time/(1000*60*60)

    return chars_sum - math.exp(exp) + 1
def chars_for_score(chars):
    chars = np.array(chars)
    chars = chars.flatten()
    chars_sum = 0
    for char in chars:
        chars_sum += char
    return chars_sum
def get_time_stamp(json):
    return(json["origin_server_ts"])
def get_content(json):
    return(json["content"])
def get_body(json):
    return(json["content"]["body"])
def get_sender(json):
    return(json["sender"])
def get_type(json):
    return(json["type"])
def get_msgtype(json):
    return(json["content"]["msgtype"])
def valid_text_msg(json):
    return (json["type"]== "m.room.message" and json["content"]["msgtype"] == "m.text" and "m.relates_to" not in json["content"])
def get_room_id(json): 
     return(json["room_id"])
def get_event_id(json): 
     return(json["event_id"])

#oben: nützliche Funktionen
#################################################################
#unten: nur für klassischen Ansatz relevant


class Searchables:                                          #funktioniert momentan nur für einen Raum, da alle nachrichten zusammen gespeichert werden
    words = []      #Keywords einer Nachricht
    hashes = []     #Hashes der Keywords
    event = []      #gesamte Json der Nachricht

    def __init__ (self):
        return

    def add_to(self, words, hashes, event):
        self.words.append(words)
        self.hashes.append(hashes)
        self.event.append(event)
    
    def get_words(self):
        return self.words

    def get_hashes(self):
        return self.hashes

    def return_exisiting_words(self, hashes):       #returnt array, [0] ist liste der gefundenen Wörter, [1] ist Liste in welcher Nachricht diese gefunden wurden
        findings_words = []                         #               [2] returnt Events (Json der Nachricht)
        findings_nachrichtindex = []
        findings_events = []

        findings = [findings_words, findings_nachrichtindex, findings_events]

        for hash in hashes:
            ind_hashes = 0
            for saved_hashes in self.hashes:
                ind_hash = 0
                for saved_hash in saved_hashes:
                    if hash == saved_hash:
                        findings_words.append(self.words[ind_hashes][ind_hash])
                        findings_nachrichtindex.append(ind_hashes)
                        findings_events.append(self.event[ind_hashes])

                    ind_hash += 1
                ind_hashes += 1

        return findings

def get_primitive_keywords(message):
    message_without_special_keys = re.sub('[^A-Za-z0-9]+', ' ', message) #das hier wird hier vielleicht nicht gebraucht, bzw. es ist nicht ausgeschlossen dass das hier nicht was kaputt macht

    return keyWordExtraction(message_without_special_keys, "german")

    
    message_without_special_keys = re.sub('[^A-Za-z0-9]+', ' ', message)
    words_as_array = re.sub('[^\w]', ' ', message_without_special_keys).split()
    return get_usefull_primitive_keywords(words_as_array)

def get_usefull_primitive_keywords(keywords):
    usefprimkw = []

    for word in keywords:
        if(len(word) > 5):
            usefprimkw.append(word.lower())

    return usefprimkw

def keyWordExtraction(user_question: str, language):
    words = nltk.word_tokenize(user_question, language=language)
    
    key_words = []
    if(language == "german"):
        tagger = ht.HanoverTagger('morphmodel_ger.pgz')
        tagged = tagger.tag_sent(words, taglevel=1)
        
        for tag in tagged:
            if(tag[2] == "NN" or tag[2] == "NE"):
                key_words.append(tag[0].lower())    #hier noch das lowercase keyword angefügt
    elif(language == "english"):
        tagger = nltk.pos_tag(words)
        
        for tag in tagger:
            if(tag[1].startswith("NN") or tag[1].startswith("VB") or tag[1].startswith("JJ")):
               key_words.append(tag[0])
    else:
        print("language not supported")
        exit(2)
    
    return key_words

def entf_suffix(usefprimkw):
    suffixfreie_usefprimkw = []
    
    for word in usefprimkw:
        suffixfreie_usefprimkw.append(word[:])    #nutzlos, so wie ich mir das vorstelle

    return suffixfreie_usefprimkw

def hashing_suffrusefprimkw(suffixfreie_usefprimkw):
    hashes = []

    for word in suffixfreie_usefprimkw:
        hash = 0
        for ind in range(0, len(word)):
            if ind%2 == 1:
                hash += 2*ord(word[ind])
            else:
                hash += ord(word[ind])
            ind += 1
        hashes.append(hash)

    return hashes

def json_do_your_thing(event, room):        #klassische Keywordsuche, Speicherung in Liste und Keywordsuche durch Hashes
    if not valid_text_msg(event):
        return

    searchables = Searchables()

    with open('json_util/nsa_wäre_stolz.json', 'a') as jfile:
        json.dump(event, jfile)

    primkw = get_primitive_keywords(get_body(event))
    if primkw == []:
        return

    # primkw ist liste der nomen und eigennamen
    # an dieser Stelle lemma einfügen

    nlp = spacy.load("de_core_news_lg")

    suffixfreie_usefprimkw = []
    hash_suffrusefprimkw = []
    for keyw in primkw:
        doc = nlp(keyw)
        for token in doc:
            suffixfreie_usefprimkw.append(token.lemma_)
            hash_suffrusefprimkw.append(token.lemma)
            print(token.lemma_)

    #suffixfreie_usefprimkw = entf_suffix(primkw)
    #hash_suffrusefprimkw = hashing_suffrusefprimkw(suffixfreie_usefprimkw)
    exisiting_words = searchables.return_exisiting_words(hash_suffrusefprimkw)

    if exisiting_words != [[], [], []]:

        chars_of_msg = []
        exisiting_words1_set = list(dict.fromkeys(exisiting_words[1]))
        for index_of_msg in range(len(exisiting_words1_set)):
            char_of_msg = 0
         
            for ind_words in range(len(exisiting_words[0])):
                if exisiting_words1_set[index_of_msg] == exisiting_words[1][ind_words]:
                    char_of_msg += len(exisiting_words[0][ind_words])

            chars_of_msg.append(char_of_msg)


        print(chars_of_msg)
        best = 0
        score_old = score(chars_of_msg[best], get_time_stamp(event)-get_time_stamp(json.loads(exisiting_words[2][best])))
        for ind in range(len(exisiting_words1_set)):
            score_new = score(chars_of_msg[ind], get_time_stamp(event)-get_time_stamp(json.loads(exisiting_words[2][ind])))
            if score_new > score_old:
                best = ind
                score_old = score_new
        
        print("best: ", best)

        if score_old > 2:
            send_message(room, exisiting_words[2][best])

    # neue Nachricht abspeichern
    searchables.add_to(suffixfreie_usefprimkw, hash_suffrusefprimkw, json.dumps(event))



#oben: nur für klassischen Ansatz relevant
#################################################################
#unten: vollständige Schnittstelle zum Matrixchat inkl. Funktionen für I/O

def new_message_handling(event, room):
    """
        event: empfangene Json der Form     {
                                                "content": {
                                                    "body": "trauben",
                                                    "msgtype": "m.text"
                                                },
                                                "origin_server_ts": 1624286301820,
                                                "sender": "@lionn:matrix.tu-berlin.de",
                                                "type": "m.room.message",
                                                "unsigned": {
                                                    "age": 947
                                                },
                                                "event_id": "$8sDT1_34_V5tmb-fhnz-pw-RJthTCkqqW68jaSf20uM",
                                                "room_id": "!qQesPBpEHJUVpcJzxG:matrix.org"
                                            } 
        room: raumobjekt der matrix sdk, mit der eine Schnittstelle zur Vollständigen Funktionalität der Matrix sdk gewährleistet wird
    """

    #klassischer Ansatz für die Datenverarbeitung; Probleme sind u.a. skaliert nur bedingt, da Nachrichten zur Keywordsuche nur temporär gespeichert werden
    json_do_your_thing(event, room)

    # hier kann weitere Funktionalität angebunden werden
    # mit send_message(room, "json der zu referenzierenden Nachricht") kann auf eine Nachricht referenziert werden
    # mit room.send_text("hier der zu sendende Text") kann Text direkt in den Raum geschickt werden

def send_message(room, event, msgtype="m.text"):
    # room: Matrix-Raum-Objekt
    # event: zu referenzierende Nachricht als json Obket der Form die in new_event_handling gezeigt ist


    jevent = json.loads(event)
    html_msg = get_html_msg(event)
    event_id = get_event_id(jevent)
    body = '> <' + get_sender(jevent) +'>'
    #room.send_html(html_msg, body)
    return room.client.api.send_message_event(
            room.room_id, "m.room.message", get_html_content(room, html_msg, event_id, body, msgtype))


    #room.client.api.send_message_event(
            #room.room_id, "m.room.message", room.get_html_content(html, body, msgtype))

    #room.send_notice('Diese Nachricht scheint in Zusammenhang zu stehen und hilft vielleicht weiter:\n' + ursprungsnachricht)
    #room.send_text('Diese Nachricht scheint in Zusammenhang zu stehen und hilft vielleicht weiter:\n' + ursprungsnachricht)

    #https://github.com/matrix-org/matrix-python-sdk/blob/master/matrix_client/room.py
    #https://github.com/matrix-org/matrix-python-sdk/blob/master/matrix_client/api.py

def get_html_content(room, html, event_id, body=None, msgtype="m.text"):
        return {
            "body": body if body else re.sub('<[^<]+?>', '', html),
            "msgtype": msgtype,
            "format": "org.matrix.custom.html",
            "formatted_body": html,
            "m.relates_to": {
                "m.in_reply_to": {
                    "event_id": event_id
                }
            },
        }

def get_html_msg(event):
    jevent = json.loads(event)

    pref0 = '<mx-reply><blockquote><a href=\"https://chat.tu-berlin.de/#/room/'         
    roomid = get_room_id(jevent)
    pref1 = '/'
    eventid = get_event_id(jevent)
    pref2 = '?via=matrix.org&via=matrix.tu-berlin.de\"></a><a href=\"https://chat.tu-berlin.de/#/user/' #hier mlg. dynamisch homeserver des users einsetzen
    user = get_sender(jevent)
    pref3 = '\">'
    user2 = user
    pref4 = '</a><br>'
    nachricht = get_body(jevent)
    pref5 = '</blockquote></mx-reply>'
    response = 'vielleicht hilft das'

    html_msg = pref0 + roomid + pref1 + eventid + pref2 + user + pref3 + user2 + pref4 + nachricht + pref5 + response

    #resonse to in der json funktioniert nicht

    return html_msg
