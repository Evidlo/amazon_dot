import pexpect
import os
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
log = logging.getLogger(__name__)

mpsyt_screen = '/home/pi/bin/mpsyt'
prompt = '\n> '
p = pexpect.spawn(mpsyt_screen, env={"TERM": "xterm", "PATH": os.environ['PATH']})

def screen_redraw():
    # send C-a C-l to make screen redraw
    p.send('\033')
    p.send('\044')

def mpsyt_stop():
    # send newline to make the current song stop if its playing
    p.send('q')

    # clear anything already in the prompt
    p.send('\025')

    time.sleep(.25)

    # this is necessary for some reason
    p.send('\n')

def wait_prompt():
    global p
    EOF = 1

    tries = 0
    while EOF and tries < 5:
        log.debug('loop:', EOF)
        screen_redraw()
        # wait until the prompt comes back
        EOF = p.expect_exact([prompt, pexpect.EOF, pexpect.TIMEOUT], timeout=10)
        if EOF == 1 or EOF == 2:
            p = pexpect.spawnu(mpsyt_screen, env={"TERM": "xterm", "PATH": os.environ['PATH']})
            time.sleep(1)
        tries += 1


def mpsyt_play(request, playlist_number=1, playlist=False):
    # send newline to make the current song stop if its playing
    p.send('q')

    wait_prompt()

    # clear anything already in the prompt
    p.send('\025')

    if playlist:
        p.sendline('//' + request)
        wait_prompt()
        p.sendline(str(playlist_number))
        wait_prompt()
        p.sendline('*')
    else:
        p.sendline('/' + request)
        wait_prompt()
        p.sendline('1')

def mpsyt_next():
    # go to next song
    p.send('>')

def mpsyt_pause():
    # pause current playback
    p.send('p')

def mpsyt_resume():
    # resume current playback
    p.send('p')
