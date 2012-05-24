import bottle
import configparser
from Rishi.corpuses.classFinder import ClassFinder
from Rishi.mind import Mind
from Rishi.corpuses.scopeTracer import ScopeTracer


__author__ = 'Robur'


class App():
    def __init__(self):


        config = configparser.ConfigParser()
        config.read('config/config.ini')


        self.mind = Mind()
        self.mind.setSources(config['Rishi']['sources'])
        self.initRoutes()
        self.mind.loadAST()


    def initRoutes(self):
        bottle.route('/mind/sourcesList')(self.getSourcesList)


    def getSourcesList(self):
        return self.mind.getSourcesList()


    def devRun(self):
        classFinder = ClassFinder()
        scopeTracer = ScopeTracer()
        self.mind.addFindCorpus(scopeTracer)
        self.mind.addFindCorpus(classFinder)
        self.mind.findHidden()
