##############################Lions dumme Idee#####################################################
import random
import re
import time

import py2neo.database
from matrix_bot_api.matrix_bot_api import MatrixBotAPI
from matrix_bot_api.mregex_handler import MRegexHandler
from matrix_bot_api.mcommand_handler import MCommandHandler

from neo4j import GraphDatabase
# noinspection PyUnresolvedReferences
from py2neo import Graph

if __name__ == '__main__':

    gs = Graph("bolt://localhost:7687", auth=("neo4j", "TUTORAI"))

    def bot_callback(room, event):
        body = event["content"]["body"]
        nachricht = body[5:len(body)]  # cutted die nachricht
        print(nachricht)

        room.send_text(str(gs.run(nachricht).data()))
        #room.send_text('ich hab mal was für dich rausgesucht:\n' + resp)


    USERNAME = "kleiner_bot"
    PASSWORD = "MatrixBotPasswort123"
    SERVER = "https://matrix-client.matrix.org"

    bot = MatrixBotAPI(USERNAME, PASSWORD, SERVER)

    bot_handler = MRegexHandler("!bot", bot_callback)
    bot.add_handler(bot_handler)

    bot_handler = MRegexHandler("!Bot", bot_callback)
    bot.add_handler(bot_handler)

    # Bot startet

    bot.start_polling()
    print("bot is ready")

    # ka ob das noch gebraucht wird
    while True:
        input()


    # Anfrage in Matrix



###################################################################################################