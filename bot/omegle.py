#!/usr/bin/env python3

# py-omelge provides a class to interface with the site Omegle. The class uses
# a simple event-callback interface and enables you to do everything the omegle
# browser client can do. You can run concurrent chats - each one is threaded.

# This is a modified version of py-omelge, for use specifically with the Omegle
# social experiment. Key modifications include:

#   * Bug Fixes
#   * PEP 8 compliance
#   * Port to Python 3

# Copyright (c) 2014 Bobng/Nigg/Lobe/etc & Joshua Fogg

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import urllib
import urllib.request
import urllib.error
import thread
import simplejson
import cookielib
import time

ua_osystem = "Windows; U; Windows NT 6.0; en-GB; rv:1.9.1.3"
ua_browser = "Gecko/20090824 Firefox/3.5.3"
user_agent = "Mozilla/5.0 ({0}) {1}".format(ua_osystem, ua_browser)


class EventHandler:
    def fire(self, event, chat, var):
        '''Callback class. Var is info relating to the event'''
        if hasattr(self, event):
            getattr(self, event)(chat, var)


class OmegleChat:
    def __init__(self, _id=None, debug=False):
        self.url = "http://omegle.com/"
        self.id = _id
        self.failed = False
        self.connected = False
        self.in_chat = False
        self.handlers = []
        self.terminated = False

        self.debug = debug

        jar = cookielib.CookieJar()
        processor = urllib.request.HTTPCookieProcessor(jar)
        self.connector = urllib.request.build_opener(processor)
        # , urllib.request.HTTPHandler(debuglevel=1))
        self.connector.addheaders = [
            ('User-agent', user_agent)
            ]

    def pausedChat(self, chat, message, pause):
        '''Make it look like the bot is typing something'''
        self.typing()
        time.sleep(pause)
        self.stoppedTyping()
        self.say(message)

    def get_events(self, json=False):
        '''Poll the /events/ page and process the response'''
        # requester = urllib.request.Request(self.url + 'events',
        #                             headers={'id':self.id})
        dataURL = urllib.urlencode({'id': self.id})
        events = self.connector.open(self.url+'events', data=dataURL).read()
        if json:
            return simplejson.loads(events)
        else:
            return events

    def connect_events(self, event_handler):
        '''Add an event handler'''
        self.handlers.append(event_handler)

    def fire(self, event, var):
        for handler in self.handlers:
            handler.fire(event, self, var)

    def terminate(self):
        '''Terminate the thread.
        Don't call directly, use .disconnect() instead'''
        self.terminated = True

    def open_page(self, page, data={}):
        if self.terminated:
            return

        if 'id' not in data:
            data['id'] = self.id
        r = self.connector.open(self.url + page, urllib.urlencode(data)).read()
        if r != "win":
            # Maybe make it except here?
            if self.debug:
                print('Page {0} returned {1}'.format(page, r))
        return r

    def say(self, message):
        '''Send a message from the chat'''
        if self.debug:
            print('Saying message:', message)
        self.open_page('send', {'msg': message})

    def disconnect(self):
        '''Close the chat'''
        self.open_page('disconnect', {})
        self.terminate()

    def typing(self):
        '''Tell the stranger we are typing'''
        self.open_page('typing')

    def stoppedTyping(self):
        '''Tell the stranger we are no longer typing'''
        self.open_page('stoppedtyping')

    def connect(self, threaded=True):
        '''Start a chat session'''
        if not self.id:
            self.id = self.connector.open(self.url + 'start', data="") # {}
            self.id = self.id.read().strip('"')

        self.connected = True
        if threaded:
            thread.start_new_thread(self.reactor, ())
        else:
            self.reactor()

    def waitForTerminate(self):
        '''This only returns when .disconnect() or .terminate() is called'''
        while not self.terminated:
            time.sleep(0.1)
            pass
        return

    def reactor(self):
        while True:
            if self.terminated:
                if self.debug:
                    print("Thread terminating")
                return

            events = self.get_events(json=True)
            if not events:
                continue
            if self.debug:
                print(events)
            for event in events:
                if len(event) > 1:
                    self.fire(event[0], event[1:])
                else:
                    self.fire(event[0], None)

if __name__ == '__main__':

    class MyEventHandler(EventHandler):
        def connected(self, chat, var):
            print("Connected")
            chat.in_chat = True
            chat.say("Hello!")

        def gotMessage(self, chat, message):
            message = message[0]
            print("Message recieved:", message)

        def typing(self, chat, var):
            print("Stranger is typing...")

        def stoppedTyping(self, chat, var):
            print("Stranger stopped typing!")

        def strangerDisconnected(self, chat, var):
            print("Stranger disconnected - Terminating")
            chat.terminate()

    for i in xrange(2):
        print("Starting chat", i)
        a = OmegleChat()
        a.connect_events(MyEventHandler())
        a.connect(True)
        a.waitForTerminate()
    raw_input()
