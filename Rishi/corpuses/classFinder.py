from Rishi.corpuses.walkerCorpus import WalkerCorpus
from Rishi.parser import AST

__author__ = 'Robur'

class Object:
    def __init__(self, name):
        self.NS = None
        self.name = name
        self.children = []


class ClassFinder(WalkerCorpus):
    def __init__(self, objects):
        self.objects = objects

    def prepareToWalk(self,state, root):
        pass

    def enterNode(self,node,state):
        if isinstance(node,AST.AssignmentExpression) and node.op == '=' and isinstance(node.right, AST.FunctionExpression):
            refs = AST.toLeftSideRefs(node.left)
            if not len(refs): return
            if 'prototype' in refs:
                self.createClass(refs[:refs.index('prototype')])

    def createClass(self, name):
        objects = self.objects
        doneSearch = False
        while not doneSearch and len(name):
            doneSearch = True
            for cl in objects:
                if cl.name == name[0]:
                    objects = cl.children
                    name = name[1:]
                    doneSearch = False
                    break
        while len(name):
            print(name)
            cl = Object(name[0])
            objects.append(cl)
            objects = cl.children
            name = name[1:]
            
#            for prop in refs[1:]:





