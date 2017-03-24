from flask_ask import Ask, statement, question, session
from flask import Flask
from random import randint

# from OpenSSL import SSL
# context = SSL.Context(SSL.SSLv23_METHOD)
# context.use_privatekey_file('private-key.pem')
# context.use_certificate_file('cert.pem')

import random

numbers = None

app = Flask(__name__)
# app.config['ASK_VERIFY_REQUESTS'] = False

ask = Ask(app, "/")

@ask.launch
def launch():
    return question("welcome to evans alexa app.  are you ready?")

@ask.intent("YesIntent")
def test():
    global numbers
    numbers = (randint(0,9), randint(0,9))
    return question("what is {} plus {}".format(numbers[0], numbers[1]))

@ask.intent("AnswerIntent", convert={'response':int})
def answer(response):
    print(response)
    if response == numbers[0] + numbers[1]:
        msg = "you win"
    else:
        msg = "you lose" 

    return statement(msg)

@ask.intent("IRCIntent")
def randomthing():
    return statement("I sent the message")

@ask.intent("PlayIntent", convert={'request':str})
def answer(request):
    print(request)
    return statement("you said {}".format(request))


if __name__ == '__main__':
        app.run(debug=True, host='0.0.0.0', ssl_context=('cert.pem', 'private-key.pem'))


