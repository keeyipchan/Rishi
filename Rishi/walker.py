from Rishi.parser import AST

__author__ = 'Robur'


class Walker:
    def __init__(self):
        self.ast = None
        self.watchers = []
        self.state = None

    def setAst(self, ast):
        self.ast = ast

    def walk(self):
        self.state = {}
        for watcher in self.watchers:
            watcher.prepareToWalk(self.state, self.ast)
        self.lookToNode(self.ast)

#        print(self.state)

    def lookToNode(self, node, level = 0):
#        print(str(type(node)))
        for watcher in self.watchers:
            watcher.enterNode(node,self.state)
        props = node.__dict__
        for prop in props:
            if prop == 'parent': continue
#            print((" "*level*4) +prop, end=': ')
            if isinstance(props[prop], AST.Node):
                self.lookToNode(props[prop], level+1)
            elif isinstance(props[prop], list):
                for item in props[prop]:
                    if isinstance(item, AST.Node):
                        self.lookToNode(item, level+1)
#                    else:
#                        print(str(item),end=",")

#                print("")
#            else:
#                print(str(props[prop]))
        for watcher in self.watchers:
            watcher.exitNode(node,self.state)


    def addWatcher(self, watcher):
        self.watchers.append(watcher)