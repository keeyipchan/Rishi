__author__ = 'Robur'
import sys,os
path = os.path.dirname(__file__)
if not path in sys.path:
    sys.path.insert(0,path)

print(sys.path)

# Change working directory so relative paths (and template lookup) work again
os.chdir(os.path.dirname(__file__))

import bottle
bottle.debug(True)
from Rishi.init import start

start()


application = bottle.default_app()


