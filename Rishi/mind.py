import json
import os

__author__ = 'Robur'

class Serializable:
    def toDict(self):
        return 'Class serialization not implemented: '+type(self).__name__

class SourceFile(Serializable):
    def __init__(self, path, parsed = False):
        self.path = path
        self.parsed = False

from Rishi.jsonEncoder import JsonEncoder
jsonEncoder = JsonEncoder()

class Mind() :
    def __init__(self):
        self.sources = ''
        self.sourceList = []

    def setSources(self, sources):
        self.sources = sources
        self.sourceList = []
        for file in os.listdir(sources):
            name = file.split('.')
            if name[len(name)-1] == 'js':
                self.sourceList.append(SourceFile(file))
    def getSourcesList(self):
        return jsonEncoder.encode(self.sourceList)

    def updateParseCache(self):
        for file in self.sourceList:
            self.updateFile(file)

    def updateFile(self, file):
        from Rishi.parser.JSParser import Parser
        parser = Parser()
        parsed = self.sources + file+'.ast'
        if os.path.exists(parsed):
            parser.src = open(parsed).read()
            parser.buildAST()
