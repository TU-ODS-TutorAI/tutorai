import json
import spacy
from py2neo import Graph
import simplematrixbotlib as botlib
import re
import matrix_util.matrix_util as mutil
from backend.matrix import json_util as jutil
from urllib.request import urlopen

USERNAME = "kleiner_bot"
PASSWORD = "MatrixBotPasswort123"
SERVER = "https://matrix-client.matrix.org"
NEO4JPASSWORD = "TUTORAI"
neo4j = Graph("bolt://localhost:7687", auth=("neo4j", NEO4JPASSWORD))
nlp = spacy.load("de_core_news_lg")
with open('Preset_Config.json') as json_file:
    presetConfig = json.load(json_file)
LANGUAGE = 1

"""
Initialize Bot
"""
PREFIX = '!'
creds = botlib.Creds(SERVER, USERNAME, PASSWORD)
bot = botlib.Bot(creds)

# https://matrix.org/docs/spec/client_server/latest#id43


async def volltextsuche_moses(room, message):
    nachricht = message.body[18:]
    nachricht = re.sub('[^A-Za-z0-9\-]+', ' ', nachricht)
    print(nachricht)

    nachricht = nachricht.replace(" ", "+")
    url = "http://localhost:3000/moses/search/german.content?q="  # pagenotfound
    resp_json = urlopen(url + nachricht)  # bei mehr wörtern einfach leer durch + ersetzen
    resp = json.loads(resp_json.read())

    resp_to_text = ''
    ct = 0
    for reg in resp:
        resp_to_text += str(reg["german"]["title"])
        resp_to_text += ": " + "https://moseskonto.tu-berlin.de/moses/modultransfersystem/bolognamodule/beschreibung/anzeigen.html?nummer="
        resp_to_text += str(reg["number"])
        resp_to_text += "&version="
        resp_to_text += str(reg["version"])
        resp_to_text += "&sprache=1\n"

        ct += 1
        if ct > 2:
            resp_to_text += '...\n\n und in vielen mehr. Bitte konkretisiere deine Suche etwas.'
            break
        if ct > 1:
            resp_to_text += ', '

    if ct == 0:
        await mutil.send_notice_message(bot, room.room_id, 'Leider war die Suche Erfolglos')
    elif ct < 2:
        await mutil.send_notice_message(bot, room.room_id, 'Ich habe dazu etwas in diesem Modul gefunden:\n' + resp_to_text)
    else:
        await mutil.send_notice_message(bot, room.room_id, 'Ich habe dazu etwas in diesen Modulen gefunden:\n' + resp_to_text)


async def neo4j_volltextsuche(room, message):
    # room: raum-objekt der matrix-sdk
    # nachricht ohne das initiale !volltext
    nachricht = message.body[9:]

    doc = nlp(nachricht)
    search_results = []
    for token in doc:
        if token.pos_ != "PUNCT" and token.pos_ != "SPACE":
            for name in neo4j.run(
                    f"match (v:volltext {{lemma:'{token.lemma}'}})-[:`GEHÖRT_ZU`]-(a) return a.name, a.Version, a.Modulnummer").data():
                if str(name["a.name"]) not in search_results:
                    search_results.append(name['a.name'] + ":" +
                                            f"https://moseskonto.tu-berlin.de/moses/modultransfersystem/bolognamodule/beschreibung/anzeigen.html?nummer={name['a.Modulnummer']}&version={name['a.Version']}&sprache={LANGUAGE}")
            for name in neo4j.run(
                    f"match (v:volltext {{text:'{token.text.lower()}'}})-[:`GEHÖRT_ZU`]-(b) return b.name, b.Version, b.Modulnummer").data():
                if str(name["b.name"]) not in search_results:
                    search_results.append(name['b.name'] + ":" +
                                          f"https://moseskonto.tu-berlin.de/moses/modultransfersystem/bolognamodule/beschreibung/anzeigen.html?nummer={name['b.Modulnummer']}&version={name['b.Version']}&sprache={LANGUAGE}")

    if len(search_results) == 0:
        await mutil.send_notice_message(bot, room.room_id, 'Leider war die Suche Erfolglos')
    elif len(search_results) < 2:
        await mutil.send_notice_message(bot, room.room_id, 'Ich habe dazu etwas in diesem Modul gefunden:\n' + ',\n'.join(search_results))
    elif len(search_results) > 10:
        await mutil.send_notice_message(bot, room.room_id, 'Ich habe dazu etwas in diesen Modulen gefunden:\n' + ',\n'.join(search_results[:10]) + '\nund in vielen mehr. Bitte konkretisiere deine Suche etwas.')
    else:
        await mutil.send_notice_message(bot, room.room_id, 'Ich habe dazu etwas in diesen Modulen gefunden:\n' + ',\n'.join(search_results))


# wird ausgeführt auch wenn der Bot nicht angesprochen wird
async def bot_callback_uncalled(room, event):
    await jutil.new_message_handling(bot, event, room, neo4j, nlp)


# Handles an isis search
def isis_suche(room, event):
    print("not yet implemented")


# Event_Handlers und Main Thread
# Handles all the preset ways the bot interacts
async def bot_callback_preset(room, message):
    match = botlib.MessageMatch(room, message, bot)

    if match.not_from_this_bot() and match.prefix(PREFIX):
        if match.command("volltext"):
            await neo4j_volltextsuche(room, message)
        elif match.command("volltext_klassik"):
            await volltextsuche_moses(room, message)
        elif match.command("isis"):
            isis_suche(room, message)
        elif match.command("echo"):
            await mutil.send_notice_message(bot, room.room_id, message.body)
        else:
            for inquiry in presetConfig:
                if match.command(inquiry):
                    await mutil.send_notice_message(bot, room.room_id, presetConfig[inquiry])
    else:
        await bot_callback_uncalled(room, message)


def main():

    bot.add_message_listener(bot_callback_preset)

    bot.run()
    print("bot is ready")


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
# https://matrix.org/docs/spec/client_server/latest#m-notice