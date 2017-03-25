import pexpect
import time

mpsyt_screen = '/home/pi/bin/mpsyt'

p = pexpect.spawnu(mpsyt_screen, env={"TERM": "xterm"})

def mpsyt_stop():
    # send newline to make the current song stop if its playing
    p.sendline('')


def mpsyt_play(request, playlist_number=1, playlist=False):
    # send newline to make the current song stop if its playing
    p.sendline('')

    time.sleep(1)

    # wait until the prompt comes back
    p.expect_exact([prompt], timeout=10)

    # clear anything already in the prompt
    p.send('\025')

    if playlist:
        p.sendline('//' + request)
        p.sendline(str(playlist_number))
        p.sendline('*')
    else:
        p.sendline('/' + request)
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
