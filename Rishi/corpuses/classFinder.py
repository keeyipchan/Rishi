import Object
from Rishi.corpuses.walkerCorpus import WalkerCorpus
from Rishi.parser import AST

__author__ = 'Robur'


class ClassFinder(WalkerCorpus):
    def __init__(self, glob=None, classes=None):
        if classes == None: classes = {}
        if glob == None:
            glob = Object.Object('<global>')
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

        if isinstance(node, AST.Call) and isinstance(node.expr, AST.Property):
            #convert all this.z()... nodes to method
            refs = AST.toLeftSideRefs(node.expr)
            if refs[0] == 'this' and len(refs) == 2 and self.scope.node != None: #not a global scope (it possible, but must not happen)
                obj = self.scope
                if obj.isMethod():
                    method = obj.parent.ensureObject(refs[1])
                    method.setMethodType()
                else:
                    if not obj.isClass():
                        obj.setClassType()
                        self.addClass(obj)
                    method = obj.ensureObject(refs[1])
                    method.setMethodType()


        if isinstance(node, AST.Property):
            #convert all this.z.x... nodes to property
            refs = AST.toLeftSideRefs(node)
            if refs[0] == 'this' and len(refs) > 1 and self.scope.node != None: #not a global scope (it possible, but must not happen)
                obj = self.scope
                if obj.isMethod():
                    prop = obj.parent.ensureObject(refs[1])
                    if prop.isGeneric():
                        prop.setPropertyType()
                else:
                    if not obj.isClass():
                        obj.setClassType()
                        self.addClass(obj)
                    prop = obj.ensureObject(refs[1])
                    if prop.isGeneric():
                        prop.setPropertyType()

        if isinstance(node, AST.FunctionExpression) or isinstance(node, AST.FunctionDeclaration):
            #open new scope
            if node.obj != None:
                #predefined linked object from previous parsing - used as a scope
                node.obj.outerScope = self.scope
                self.scope = node.obj
            else:
                #create new scope object
                if node.name != None: name = node.name
                else: name = '<anonymous>'
                node.obj = Object.Object(name)
                node.obj.outerScope = self.scope
                self.scope = node.obj


        if isinstance(node, AST.New):
            #simple constructor handling
            refs = AST.toLeftSideRefs(node.expr)
            if len(refs):
                obj = self.scope
                obj.setLink('create', self.globalObj.ensureObject(refs))


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




