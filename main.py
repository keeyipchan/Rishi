from Rishi.app import App

__author__ = 'Robur'

import bottle


app = App()

bottle.debug(True)
bottle.run(host='localhost', port=8080, reloader=True)


#import sys,os
#path = os.path.dirname(__file__)
#if not path in sys.path:
#    sys.path.insert(0,path)
#
#print(sys.path)
#
## Change working directory so relative paths (and template lookup) work again
#os.chdir(os.path.dirname(__file__))
#
#import bottle
#bottle.debug(True)
#
#from Rishi.init import start
#
#start()
#
#
#application = bottle.default_app()
#

