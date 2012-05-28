from Rishi.corpuses.walkerCorpus import WalkerCorpus
from Rishi.parser import AST

__author__ = 'Robur'

class Object:
    def __init__(self, name):
        self.name = name
        self.children = []


class FunctionObject(Object):
    def __init__(self, name):
        super().__init__(name)

class PropertyObject(Object):
    def __init__(self, name):
        super().__init__(name)


class ClassObject(Object):
    def __init__(self, name):
        super().__init__(name)
        self.methods = []
        self.props = []

    def addMethod(self, name):
        self.methods.append(FunctionObject(name))

    def addProperty(self, name):
        if self.hasProperty(name): return
        self.props.append(PropertyObject(name))
        print(self.name+'.'+name)

    def hasProperty(self, name):
        for prop in self.props:
            if prop.name == name: return True
        return False


class ClassFinder(WalkerCorpus):
    def __init__(self, objects):
        self.objects = objects
        self.scope = []

    def prepareToWalk(self, state, root):
        pass

    def enterNode(self, node, state):
        #check for a.b.prototype.d = function () {..} - create objects in chain and method
        if isinstance(node, AST.AssignmentExpression) and node.op == '=' and isinstance(node.right, AST.FunctionExpression):
            refs = AST.toLeftSideRefs(node.left)
            if not len(refs): return
            if 'prototype' in refs:
                self.createClass(refs[:refs.index('prototype')])
                if refs.index('prototype') < len(refs) - 1:
                    self.createMethod(refs[:refs.index('prototype')], refs[refs.index('prototype') + 1])
        #keep track of scope
        if isinstance(node, AST.FunctionBody):
            self.scope.append(node)

        #check for access to properties  this.b.c
        if isinstance(node, AST.Property):
            refs = AST.toLeftSideRefs(node)
            if refs and refs[0] == 'this' and len(refs)>1:
                #create property for form Obj.prototype.x = function (){}
                if len(self.scope) > 0:
                    scope = self.scope[len(self.scope)-1]
                    if isinstance(scope.parent.parent, AST.AssignmentExpression) and scope.parent.parent.op == '=' and isinstance(scope.parent.parent.left, AST.Property):
                        className = AST.toLeftSideRefs(scope.parent.parent.left)
                        if className and 'prototype' in className:
                            className = className[:className.index('prototype')]
                        self.createProperty(className, refs[1])


    def exitNode(self,node,state):
        #pop scope
        if isinstance(node, AST.FunctionBody):
            self.scope.pop()


    def createClass(self, name):
        objects = self.objects
        doneSearch = False
        cl = None
        while not doneSearch and len(name):
            doneSearch = True
            for cl in objects:
                if cl.name == name[0]:
                    objects = cl.children
                    name = name[1:]
                    doneSearch = False
                    break
        while len(name):
            cl = ClassObject(name[0])
            objects.append(cl)
            objects = cl.children
            name = name[1:]
        return cl

    def createMethod(self, object, method):
        object = self.createClass(object)
        object.addMethod(method)

    def createProperty(self, className, propName):
        object = self.createClass(className)
        object.addProperty(propName)





