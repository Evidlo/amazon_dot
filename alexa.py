#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask_ask import Ask, statement, question, session
from flask import Flask
from random import randint
from subprocess import call
import os
import logging

from mpsyt_api import *

numbers = None

DIR = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)
# app.config['ASK_VERIFY_REQUESTS'] = False

ask = Ask(app, "/")

logging.basicConfig(level=logging.INFO, format='%(message)s')
log = logging.getLogger(__name__)

mpsyt_bin = '/home/pi/bin/mpsyt'
is_playing_str = '\x1b[39m] SEEK [\x1b'

@ask.intent("StopIntent")
def stop():
    msg = "stopping"
    log.info(msg)
    mpsyt_stop()
    return statement(msg)

@ask.intent("NextIntent")
def next():
    msg = "playing next song"
    log.info(msg)
    mpsyt_next()
    return statement(msg)

@ask.intent("PauseIntent")
def pause(r):
    msg = "pausing"
    log.info(msg)
    mpsyt_pause()
    return statement(msg)

@ask.intent("ResumeIntent")
def resume():
    msg = "resuming"
    log.info(msg)
    mpsyt_resume()
    return statement(msg)

@ask.intent("PlayIntent", convert={'request':str})
def play(request):
    if request is None:
        return statement("No search query given")
    msg = "playing song {}".format(request)
    log.info(msg)
    mpsyt_play(request)
    return statement(msg)

@ask.intent("PlayPlaylistIntent", convert={'request':str})
def playlist(request):
    if request is None:
        return statement("No search query given")
    msg = "playing playlist {}".format(request)
    log.info(msg)
    mpsyt_play(request, playlist=True)
    return statement(msg)

if __name__ == '__main__':
        app.run(debug=True, host='0.0.0.0', ssl_context=(DIR+'/cert.pem', DIR+'/private-key.pem'))


