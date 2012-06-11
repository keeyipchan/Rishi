import bottle
import configparser
from Rishi.mind import Mind


__author__ = 'Robur'


class App():
    def __init__(self):


        config = configparser.ConfigParser()
        config.read('config/config.ini')


        self.mind = Mind()
        self.mind.setSources(config['Rishi']['sources'])
        self.mind.setOutputDir(config['Rishi']['output'])
        self.initRoutes()
        self.mind.loadAST()


    def initRoutes(self):
        bottle.route('/mind/sourcesList')(self.getSourcesList)


    def getSourcesList(self):
        return self.mind.getSourcesList()


    def devRun(self):
        self.mind.findHidden()
        self.mind.saveObjects()
