import logging
from random import randint
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

@ask.launch

# def start() :
  # statement('my game started!')

def new_game() :
  # hi = 'Hi say yes or no '
  # return question(hi)
  new_game_msg = 'Hey guys, lets play a game. I have some math questions for you. Should we start ?'
  return question(new_game_msg)

@ask.intent("YesIntent")
def round() :
  numbers = [ randint(0,99) for _ in range(2) ]
  # round_msg = render_template('question', nums=numbers)
  round_msg = "Alright , what is %s plus %s ?" % (numbers[0],numbers[1])
  session.attributes['total'] = numbers[0] + numbers[1]
  return question(round_msg)

@ask.intent('NoIntent')
def no_intent() :
  noo = render_template('noanswer')
  return statement(noo)
  # bye = 'Then why did you wake me up ? ... Bye ...'
  # return statement(bye)

@ask.intent('FirstAnswerIntent', convert={'first': int})
def answer(first) :
  correct = session.attributes['total']
  if first == correct:
    reply = render_template('win')
  else :
    reply = render_template('over')

  return statement(reply)

if __name__ == '__main__':
  app.run(debug=True)

# MB