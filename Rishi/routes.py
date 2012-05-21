from bottle import route
from Rishi.mind import mind
__author__ = 'Robur'

@route('/sourceList')
def hello():
    return mind.getSourceList()


def init():
    return None