import os
from Object import Object
from Rishi.corpuses.classFinder import ClassFinder
from Rishi.corpuses.scopeTracer import ScopeTracer
from Rishi.walker import Walker

__author__ = 'Robur'

class Serializable:
    def toDict(self):
        return 'Class serialization not implemented: '+type(self).__name__

class SourceFile(Serializable):
    def __init__(self, path, parsed = False):
        self.path = path
        self.parsed = False
        self.ast = None
    def toDict(self):
        return {'path':self.path, 'parsed':self.parsed}
    def setAST(self, ASTRoot):
        self.ast = ASTRoot
        self.parsed = True

from Rishi.jsonSerializer import JsonSerializer
jsonSerializer = JsonSerializer()

class Mind() :
    def __init__(self):
        self.sources = ''
        self.sourceList = []
        self.walker = Walker()
        self.classes = {}
        self.glob = Object('<global>')
        self.glob.setGlobalType()

        classFinder = ClassFinder(self.glob, self.classes)

        scopeTracer = ScopeTracer()
#        self.walker.addWatcher(scopeTracer)
        self.walker.addWatcher(classFinder)

    def setSources(self, sources):
        self.sources = sources + '/'
        self.sourceList = []
        for file in os.listdir(sources):
            name = file.split('.')
            if name[len(name)-1] == 'js':
                self.sourceList.append(SourceFile(file))

    def getSourcesList(self):
        return jsonEncoder.encode(self.sourceList)

    def updateParseCache(self):
        for file in self.sourceList:
            self.updateFileAST(file)

    def updateFileAST(self, file):
        filename = self.sources + file.path
        parsed = filename + '.ast'
        AST = None
        if not os.path.exists(parsed) or os.path.getmtime(parsed) < os.path.getmtime(filename):
            from Rishi.parser.JSParser import Parser
            parser = Parser()
            parser.src = open(filename).read()
            parser.buildAST()
            import pickle
            pickle.dump(parser.ASTRoot, open(parsed,'wb'), pickle.HIGHEST_PROTOCOL)


    def loadAST(self):
        for file in self.sourceList:
            self.parseSourceFile(file)

    def parseSourceFile(self, file):
        ast = self.updateFileAST(file)
        if ast == None:
            import pickle
            filename = self.sources + file.path
            parsed = filename + '.ast'
            ast = pickle.load(open(parsed,'rb'))
        file.setAST(ast)

    def findHidden(self):
        for file in self.sourceList:
            if file.parsed and file.ast:
                print (file.path)
                self.walker.setAst(file.ast)
                self.walker.walk()

        self.saveObjects()

    def saveObjects(self):
        file = open(self.outputDir + '/ObjectTree.json','w')
        file.write(jsonSerializer.serialize(self.glob))

        file = open(self.outputDir + '/classes.json','w')
        file.write(jsonSerializer.serialize(list(self.classes.keys())))

    def setOutputDir(self, outputDir):
        self.outputDir = outputDir

