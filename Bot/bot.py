#!/usr/bin/env python2

# This is a bot which is used as a proof of concept for using Omegle as a data
# source for social experiments. The bot asks users a question at random from
# a predefined list and logs their reply, whatever it may be, to a data file.

import omegle
from time import sleep
from random import randint

phrases = [
    "Pick a number between 1 and 100",
    "Pick a number between 100 and 1"
]


class MyEventHandler(omegle.EventHandler):
    def connected(self, chat, var):
        print "Connected"
        x = randint(0, len(phrases) - 1)
        chat.say(phrases[x])
        with open("output.dat", "a") as myfile:
            myfile.write("phrase" + str(x) + "\n")

    def gotMessage(self, chat, message):
        message = message[0]
        print "Message recieved: " + message
        with open("output.dat", "a") as myfile:
            myfile.write(message + "\n")

    def typing(self, chat, var):
        print "Stranger is typing..."

    def stoppedTyping(self, chat, var):
        print "Stranger stopped typing!"

    def strangerDisconnected(self, chat, var):
        print "Stranger disconnected - Terminating"
        chat.terminate()

while True:
    chat = omegle.OmegleChat()
    chat.connect_events(MyEventHandler())
    chat.connect(threaded=True)
    # Makes sure chat times out
    sleep(10)
    chat.terminate()
