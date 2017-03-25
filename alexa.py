#!/usr/bin/env python3
from flask_ask import Ask, statement, question, session
from flask import Flask
from random import randint
from subprocess import call
import os

from mpsyt_api import *

numbers = None

DIR = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)
# app.config['ASK_VERIFY_REQUESTS'] = False

ask = Ask(app, "/")

mpsyt_bin = '/home/pi/bin/mpsyt'
is_playing_str = '\x1b[39m] SEEK [\x1b'

@ask.intent("StopIntent")
def stop():
    print('stopping')
    mpsyt_stop()
    return statement("stopping")

@ask.intent("NextIntent")
def next():
    print('playing next song')
    mpsyt_next()
    return statement("playing next song")

@ask.intent("PauseIntent")
def pause(r):
    print('pausing')
    mpsyt_pause()
    return statement("pausing")

@ask.intent("ResumeIntent")
def resume():
    print('resuming')
    mpsyt_resume()
    return statement("resuming")

@ask.intent("PlayIntent", convert={'request':str})
def play(request):
    print('playing song')
    mpsyt_play(request)
    return statement("playing song")

@ask.intent("PlayPlaylistIntent", convert={'request':str})
def playlist(request):
    print('playing playlist')
    mpsyt_play(request, playlist=True)
    return statement("playing playlist")

if __name__ == '__main__':
        app.run(debug=True, host='0.0.0.0', ssl_context=(DIR+'/cert.pem', DIR+'/private-key.pem'))


