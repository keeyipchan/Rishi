import json
import os

__author__ = 'Robur'

class Mind() :
    def __init__(self):
        print('rrrr')
        self.sources = ''
        self.sourceList = []

    def setSources(self, sources):
        self.sources = sources
        self.sourceList = []
        for file in os.listdir(sources):
            name = file.split('.')
            if name[len(name)-1] == 'js':
                self.sourceList.append(file)
    def getSourceList(self):
        return json.dumps(self.sourceList)





mind = Mind()