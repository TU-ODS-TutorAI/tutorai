import random
import re
import time
import json
import requests
import py2neo
import spacy
from py2neo import Graph

import matrix_util.matrix_util as mutil
import json_util.json_util as jutil
from urllib.request import urlopen
from matrix_util.MHandler_uncalled import MHandler_uncalled
from matrix_bot_api.matrix_bot_api import MatrixBotAPI
from matrix_bot_api.mregex_handler import MRegexHandler

USERNAME = "kleiner_bot"
PASSWORD = "MatrixBotPasswort123"
SERVER = "https://matrix-client.matrix.org"
NEO4JPASSWORD = "TUTORAI"
neo4j = Graph("bolt://localhost:7687", auth=("neo4j", NEO4JPASSWORD))
nlp = spacy.load("de_core_news_lg")
with open('Preset_Config.json') as json_file:
    presetConfig = json.load(json_file)

# https://matrix.org/docs/spec/client_server/latest#id43

# wird auf !bot oder !Bot ausgeführt
def bot_callback_called(room, event):
    # check ob die Nachricht eine Valide Textnachicht ist
    if not mutil.valid_text_msg(event):
        return

    # prints (nicht relevant)
    sender = mutil.get_sender(event)
    body = mutil.get_body(event)
    type = mutil.get_type(event)
    msgtype = mutil.get_msgtype(event)

    print(body)
    print("cought called msg by " + sender)
    print("type:    " + type)
    print("msgtype: " + msgtype)

    # Bot call wird abgeschnitten
    nachricht = body[5:len(body)]

    if nachricht == '':
        return

    # volltextsuche_moses(room, event)

    neo4j_suche(room, event)


def volltextsuche_moses(room, event):
    body = mutil.get_body(event)
    nachricht = body[5:len(body)]

    nachricht = nachricht.replace(" ", "+")
    url = "http://localhost:3000/moses/search/german.content?q="  # pagenotfound
    resp_json = urlopen(url + nachricht)  # bei mehr wörtern einfach leer durch + ersetzen
    resp = json.loads(resp_json.read())

    resp_to_text = ''
    ct = 0
    for reg in resp:
        resp_to_text += str(reg["german"]["title"])
        ct += 1
        if ct > 2:
            resp_to_text += ' und in vielen mehr. Bitte konkretisiere deine Suche etwas.'
            break
        if ct > 1:
            resp_to_text += ', '

    if ct == 0:
        room.send_text('Leider war die Suche Erfolglos')
    elif ct < 2:
        room.send_text('Ich habe dazu etwas in diesem Modul gefunden: ' + resp_to_text)
    else:
        room.send_text('Ich habe dazu etwas in diesen Modulen gefunden: \n' + resp_to_text)


def neo4j_suche(room, event):
    # room: raum-objekt der matrix-sdk
    # event: Json der Nachricht, Format: Siehe json_util.new_message_handling

    # nachricht ohne das initiale !bot
    body = mutil.get_body(event)
    nachricht = body[5:len(body)]

    # cyper

    room.send_text('Cypher Ergebnis:\n')


# wird ausgeführt auch wenn der Bot nicht angesprochen wird


def neo4j_volltextsuche(room, event):
    # room: raum-objekt der matrix-sdk
    # event: Json der Nachricht, Format: Siehe json_util.new_message_handling

    print("neo4j Volltext")

    # nachricht ohne das initiale !bot
    body = mutil.get_body(event)
    nachricht = body[9:len(body)]
    # cyper

    room.send_text('Hi: ' + nachricht)

    doc = nlp(nachricht)
    searchresults = []
    for token in doc:
        if token.pos_ != "PUNCT" and token.pos_ != "SPACE":
            for name in neo4j.run(
                    f"match (v:volltext {{lemma:'{token.lemma}'}})-[:`GEHÖRT_ZU`]-(a) return a.name").data():
                if str(name["a.name"]) not in searchresults:
                    searchresults.append(name["a.name"])
            for name in neo4j.run(
                    f"match (v:volltext {{text:'{token.text.lower()}'}})-[:`GEHÖRT_ZU`]-(b) return b.name").data():
                if str(name["b.name"]) not in searchresults:
                    searchresults.append(name["b.name"])

    if len(searchresults) == 0:
        room.send_text('Leider war die Suche Erfolglos')
    elif len(searchresults) < 2:
        room.send_text('Ich habe dazu etwas in diesem Modul gefunden: ' + ', '.join(searchresults))
    else:
        room.send_text('Ich habe dazu etwas in diesen Modulen gefunden: \n' + ', '.join(searchresults))


# wird ausgeführt auch wenn der Bot nicht angesprochen wird
def bot_callback_uncalled(room, event):
    if not mutil.valid_text_msg(event):
        return

    sender = mutil.get_sender(event)
    body = mutil.get_body(event)
    type = mutil.get_type(event)
    msgtype = mutil.get_msgtype(event)

    if body[0] == '!':
        print('not saved')
        return

    print(body)
    print("cought uncalled msg by " + sender)
    print("type:    " + type)
    print("msgtype: " + msgtype)

    jutil.new_message_handling(event, room, neo4j, nlp)

    return


# Handles an isis search
def isis_suche(room, event):
    print("not yet implemented")


# Event_Handlers und Main Thread
# Handles all the preset ways the bot interacts
def bot_callback_preset(room, event):
    print("we good!")
    preset = mutil.get_body(event)[1:].split()[0].lower()

    if preset == "volltext":
        neo4j_volltextsuche(room, event)
    elif preset == "isis":
        isis_suche(room, event)
    else:
        for inquiry in presetConfig:
            if inquiry == preset:
                room.send_text(presetConfig[inquiry])


def main():
    bot = MatrixBotAPI(USERNAME, PASSWORD, SERVER)

    # bot_handler_called_1 = MRegexHandler("!bot", bot_callback_called)
    # bot_handler_called_2 = MRegexHandler("!Bot", bot_callback_called)
    bot_handler_preset = MRegexHandler("!", bot_callback_preset)
    bot_handler_uncalled = MHandler_uncalled(bot_callback_uncalled)
    # bot_handler_volltextsuche = MRegexHandler("!volltext", neo4j_volltextsuche)

    # bot.add_handler(bot_handler_called_1)
    # bot.add_handler(bot_handler_called_2)
    bot.add_handler(bot_handler_preset)
    bot.add_handler(bot_handler_uncalled)
    # bot.add_handler(bot_handler_volltextsuche)

    bot.start_polling()
    print("bot is ready")

    while True:
        input()


if __name__ == "__main__":
    main()

# TODO:
# 1
# learn from chat
#
# 1
# have preset handlers do more than text
#
# 2
# provide api that does not use matrix (http?)
