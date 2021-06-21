import random
import re
import time
import json
import requests
import matrix_util.matrix_util as mutil
import json_util.json_util as jutil
from urllib.request import urlopen
from matrix_util.MHandler_uncalled import MHandler_uncalled
from matrix_bot_api.matrix_bot_api import MatrixBotAPI
from matrix_bot_api.mregex_handler import MRegexHandler

USERNAME = "kleiner_bot" 
PASSWORD = "MatrixBotPasswort123"  
SERVER = "https://matrix-client.matrix.org"  

# https://matrix.org/docs/spec/client_server/latest#id43
def bot_callback_called(room, event):
    if not mutil.valid_text_msg(event):
        return

    sender = mutil.get_sender(event)
    body = mutil.get_body(event)
    type = mutil.get_type(event)
    msgtype = mutil.get_msgtype(event)
    nachricht = body[5:len(body)]

    print(body)
    print("cought called msg by " + sender)
    print("type:    " + type)
    print("msgtype: " + msgtype)

    if nachricht == '':
        return
    
    #volltextsuche moses
    url = "http://localhost:3000/moses/search/german.content?q="    # pagenotfound
    resp_json = urlopen(url + nachricht)                            # bei mehr wörtern einfach leer durch + ersetzen
    #response = requests.get('http://localhost:3000/moses/search/german.content', params=)
    resp = json.loads(resp_json.read())

    resp_to_text = ''
    ct = 0
    for re in resp:
        resp_to_text += str(re["german"]["title"])
        ct += 1
        if ct > 2:
            resp_to_text += 'und viele mehr. '
            break
        if ct > 1:
            resp_to_text += ', '
    
    if ct == 0:
         room.send_text('Leider war die Suche Erfolglos')
    elif ct < 2:
        room.send_text('Ich habe dazu etwas in diesem Modul gefunden: ' + resp_to_text)
    else:
        room.send_text('Ich habe dazu etwas in diesen Modulen gefunden: \n' + resp_to_text)


    return

    #cyper
    with driver.session() as session:
            resp = session.write_transaction(ask_for_modul, nachricht, 1)
    
    room.send_text('Cypher Ergebnis:\n' + resp)


       
def bot_callback_uncalled(room, event):
    if not mutil.valid_text_msg(event):
        return

    sender = mutil.get_sender(event)
    body = mutil.get_body(event)
    type = mutil.get_type(event)
    msgtype = mutil.get_msgtype(event)

    print(body)
    print("cought uncalled msg by " + sender)
    print("type:    " + type)
    print("msgtype: " + msgtype)

    if body[0] == '!':
        print('not saved')
        return

    jutil.json_do_your_thing(event, room)

    return


def main():
    bot = MatrixBotAPI(USERNAME, PASSWORD, SERVER)

    bot_handler_called_1 = MRegexHandler("!bot", bot_callback_called)
    bot_handler_called_2 = MRegexHandler("!Bot", bot_callback_called)
    bot_handler_uncalled = MHandler_uncalled(bot_callback_uncalled)

    bot.add_handler(bot_handler_called_1)
    bot.add_handler(bot_handler_called_2)
    bot.add_handler(bot_handler_uncalled)

    bot.start_polling()
    print("bot is ready")

    while True:
        input()


if __name__ == "__main__":
    main()


