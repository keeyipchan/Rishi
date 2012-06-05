from Rishi.corpuses.walkerCorpus import WalkerCorpus
from Rishi.parser import AST

__author__ = 'Robur'

class Object:
    def __init__(self, name, parent=None):
        self.name = name
        self.fields = {}
        self.node = None
        self.type = None
        self.parent = parent


    def ensureObject(self, uri):
        """
        uri in string or list form
        """
        if isinstance(uri, str):
            uri = uri.split('.')
        if not len(uri):
            raise ValueError('check of empty property')
        if not uri[0] in self.fields:
            self.fields[uri[0]] = Object(uri[0], self)
        if len(uri) > 1:
            return self.fields[uri[0]].ensureObject(uri[1:])
        return self.fields[uri[0]]

    def getObject(self, uri):
        if not len(uri):
            raise ValueError('check of empty property')
        if uri[0] in self.fields:
            if len(uri) == 1: return self.fields[uri[0]]
            else: return self.fields[uri[0]].getObject(uri[1:])
        return None

    def _setType(self, type):
        if self.type != None:
            raise ValueError('Trying to set a type of non-generic object: current %s, new %s' % (self.type, type))
        self.type = type


    def setClassType(self):
        self._setType('class')

    def setMethodType(self):
        self._setType('method')

    def setPropertyType(self):
        self._setType('property')

    def isClass(self):
        return self.type == 'class'

    def isMethod(self):
        return self.type == 'method'

    def isProperty(self):
        return self.type == 'property'

#class ClassObject(Object):
#    def __init__(self, name):
#        super().__init__(name)
#        self.methods = []
#        self.props = []
#
#    def addMethod(self, name):
#        self.methods.append(FunctionObject(name))
#
#    def addProperty(self, name):
#        if self.hasProperty(name): return
#        self.props.append(PropertyObject(name))
#        print(self.name+'.'+name)
#
#    def hasProperty(self, name):
#        for prop in self.props:
#            if prop.name == name: return True
#        return False


class ClassFinder(WalkerCorpus):
    def __init__(self, glob=Object('<global>'), classes=None):
        if not classes: classes = {}
        self.globalObj = glob
        self.classes = classes

    def prepareToWalk(self, state, root):
        pass

    def enterNode(self, node, state):
        #check for a.b.prototype.d = function () {..} - create objects in chain and method
        if isinstance(node, AST.AssignmentExpression) and node.op == '=' and isinstance(node.right, AST.FunctionExpression):
            refs = AST.toLeftSideRefs(node.left)
            if not len(refs): return
            #totally skip 'this.x.x' references (will be handled in different way(
            if refs[0] == 'this': return
            if 'prototype' in refs:
                self.ensureClass(refs[:refs.index('prototype')])
                if refs.index('prototype') < len(refs) - 1:
                    method = self.ensureMethod(refs[:refs.index('prototype')], refs[refs.index('prototype') + 1])
                    method.node = node.right
            else:
                #no 'prototype' in property chain - create just an object
                obj = self.globalObj.ensureObject(refs)
                obj.node = node.right

    #    def enterNode(self, node, state):

    def ensureClass(self, uri):
        """
        uri in array form
        """
        self.globalObj.ensureObject(uri)
        obj = self.globalObj.getObject(uri)
        obj.setClassType()
        strUri = '.'.join(uri)
        if not strUri in self.classes:
            self.classes[strUri] = obj
        return obj


    def getClass(self, uri):
        """
            uri in string or list form
        """
        if isinstance(uri, list):
            uri = '.'.join(uri)
        if uri in self.classes:
            return self.classes[uri]
        return None

    def ensureMethod(self, objUri, name):
        obj = self.getClass(objUri)
        method = obj.ensureObject(name)
        method.setMethodType()
        return method


    def analyzeClassNodes(self):
        for cl in self.classes:
            clazz = self.classes[cl]
            if not clazz.node: continue
            props = AST.extractNodes(clazz.node, AST.Property, goDeeper=False)
            for node in props:
                refs = AST.toLeftSideRefs(node)
                if len(refs)>1 and refs[0] == 'this':
                    prop = clazz.ensureObject(refs[1])
                    prop.setPropertyType()


#        #check for a.b.prototype.d = function () {..} - create objects in chain and method
#        if isinstance(node, AST.AssignmentExpression) and node.op == '=' and isinstance(node.right, AST.FunctionExpression):
#            refs = AST.toLeftSideRefs(node.left)
#            if not len(refs): return
#            if 'prototype' in refs:
#                self.createClass(refs[:refs.index('prototype')])
#                if refs.index('prototype') < len(refs) - 1:
#                    self.createMethod(refs[:refs.index('prototype')], refs[refs.index('prototype') + 1])
#        #keep track of scope
#        if isinstance(node, AST.FunctionBody):
#            self.scope.append(node)
#
#        #check for access to properties  this.b.c
#        if isinstance(node, AST.Property):
#            refs = AST.toLeftSideRefs(node)
#            if refs and refs[0] == 'this' and len(refs)>1:
#                #create property for form Obj.prototype.x = function (){}
#                if len(self.scope) > 0:
#                    scope = self.scope[len(self.scope)-1]
#                    if isinstance(scope.parent.parent, AST.AssignmentExpression) and scope.parent.parent.op == '=' and isinstance(scope.parent.parent.left, AST.Property):
#                        className = AST.toLeftSideRefs(scope.parent.parent.left)
#                        if className and 'prototype' in className:
#                            className = className[:className.index('prototype')]
#                        self.createProperty(className, refs[1])
#
#
#    def exitNode(self,node,state):
#        #pop scope
#        if isinstance(node, AST.FunctionBody):
#            self.scope.pop()
#
#
#    def createClass(self, name):
#        objects = self.objects
#        doneSearch = False
#        cl = None
#        while not doneSearch and len(name):
#            doneSearch = True
#            for cl in objects:
#                if cl.name == name[0]:
#                    objects = cl.children
#                    name = name[1:]
#                    doneSearch = False
#                    break
#        while len(name):
#            cl = ClassObject(name[0])
#            objects.append(cl)
#            objects = cl.children
#            name = name[1:]
#        return cl
#
#    def createMethod(self, object, method):
#        object = self.createClass(object)
#        object.addMethod(method)
#
#    def createProperty(self, className, propName):
#        object = self.createClass(className)
#        object.addProperty(propName)
#




