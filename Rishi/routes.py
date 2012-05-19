from bottle import route
__author__ = 'Robur'

@route('/')
def hello():
    return 'Hello World'

def init ():
    #dummy to prevent 'unused imports' detection... todo: avoid this somehow?
    pass

