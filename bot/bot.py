#!/usr/bin/env python3

import omegle

class MyEventHandler(omegle.EventHandler):
   def connected(self,chat,var):
      print("Connected")
      chat.say("Hello! I am a python bot! Who are you?")

   def gotMessage(self,chat,message):
      message = message[0]
      print("Message recieved:", message)          

   def typing(self,chat,var):
      print("Stranger is typing...")

   def stoppedTyping(self,chat,var):
      print("Stranger stopped typing!")

   def strangerDisconnected(self,chat,var):
      print("Stranger disconnected - Terminating")
      chat.terminate()

# Lets make two chats

chat = omegle.OmegleChat()
chat.connect_events(MyEventHandler())
chat.connect(threaded=True)

chat2 = omegle.OmegleChat()
chat2.connect_events(MyEventHandler())
chat2.connect(threaded=True)

raw_input()