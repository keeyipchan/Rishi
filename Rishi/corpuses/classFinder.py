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
        #every link is a tuple (type, obj)
        self.links = []

    def getURI(self):
        uri = []
        obj = self
        while obj.parent:
            uri.insert(0,obj.name)
            obj = obj.parent
        return '.'.join(uri)

    def setLink(self, type, obj):
        if self.isGlobal(): return
        if not len(list(filter(lambda link: link['type'] == type and link['obj'] == obj,self.links))):
            self.links.append({'type':type,'obj':obj})
            if self.isMethod() or self.isProperty():
                self.parent.setLink(type,obj)

    def setNode(self, node):
        self.node = node
        if node.obj != None:
            raise Exception('node already has a associated object!')
        node.obj = self

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
        if self.type != None and type != self.type:
            raise ValueError('Trying to set a type of non-generic object: current %s, new %s' % (self.type, type))
        self.type = type


    def setClassType(self):
        self._setType('class')

    def isClass(self):
        return self.type == 'class'

    def setGlobalType(self):
        self._setType('global')

    def isGlobal(self):
        return self.type == 'global'

    def setMethodType(self):
        self._setType('method')

    def isMethod(self):
        return self.type == 'method'

    def setPropertyType(self):
        self._setType('property')

    def isProperty(self):
        return self.type == 'property'


    def getMethods(self):
        return filter(lambda field: field.isMethod(), self.fields.values())

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

#class Scope:
#    def __init__(self, outer=None, obj=None):
#        self.outer = outer
#        self.obj = obj


class ClassFinder(WalkerCorpus):
    def __init__(self, glob=None, classes=None):
        if not classes: classes = {}
        if glob == None:
            glob = Object('<global>')
            glob.setGlobalType()
        self.globalObj = glob
        self.classes = classes
        self.scope = glob

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
                    method.setNode(node.right)
            else:
                #no 'prototype' in property chain - create just an object
                obj = self.globalObj.ensureObject(refs)
                obj.setNode(node.right)

        if isinstance(node, AST.Property):
            refs = AST.toLeftSideRefs(node)
            if refs[0] == 'this' and len(refs) > 1 and self.scope.node != None: #not a global scope (it possible, but must not happen)
                obj = self.scope
                if obj.isMethod():
                    prop = obj.parent.ensureObject(refs[1])
                    prop.setPropertyType()
                else:
                    if not obj.isClass():
                        obj.setClassType()
                        self.addClass(obj)
                    prop = obj.ensureObject(refs[1])
                    prop.setPropertyType()

        if isinstance(node, AST.FunctionExpression) or isinstance(node, AST.FunctionDeclaration):
            #open new scope
            if node.obj != None:
                node.obj.outerScope = self.scope
                self.scope = node.obj

        if isinstance(node, AST.New):
            #simple constructor handling
            refs = AST.toLeftSideRefs(node.expr)
            obj = self.scope
            obj.setLink('create', self.globalObj.getObject(refs))


    def exitNode(self,node,state):
        if isinstance(node, AST.FunctionExpression) or isinstance(node, AST.FunctionDeclaration):
            #close current scope
            if self.scope.outerScope != None:
                self.scope = self.scope.outerScope


    def ensureClass(self, uri):
        """
        uri in array form
        """
        self.globalObj.ensureObject(uri)
        obj = self.globalObj.getObject(uri)
        obj.setClassType()
        self.addClass(obj)
        return obj

    def addClass(self, obj):
        strUri = obj.getURI()
        if not strUri in self.classes:
            self.classes[strUri] = obj

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


#    def analyzeClassNodes(self):
#        for cl in self.classes:
#            clazz = self.classes[cl]
#            if clazz.node:
#                self.extractThisProperties(clazz.node, clazz)
#
#            for method in list(clazz.getMethods()):
#                self.extractThisProperties(method.node, clazz)
#
#
#    def extractThisProperties(self, node, clazz):
#        props = AST.extractNodes(node, AST.Property, goDeeper=False)
#        for node in props:
#            refs = AST.toLeftSideRefs(node)
#            if len(refs) > 1 and refs[0] == 'this':
#                prop = clazz.ensureObject(refs[1])
#                prop.setPropertyType()

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




