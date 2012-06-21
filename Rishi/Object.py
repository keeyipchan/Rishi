__author__ = 'Robur'


#type can be converted only by increasing the level
# Object  -> Property  ... -> Class  ...
types = ['generic', 'global', 'property','method','class']


class Object:
    def __init__(self, name, parent=None):
        self.name = name
        self.fields = {}
        self.node = None
        self.type = types[0]
        self.parent = parent
        #every link is a tuple (type, obj)
        self.links = []

    def forJSON(self):
        return {name:self.name}

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
        if self.type != None and types.index(type) < types.index(self.type):
            raise ValueError('Trying to decrease type level: current %s, new %s' % (self.type, type))
        self.type = type


    def isGeneric(self):
        return self.type == types[0]

    def setGlobalType(self):
        self._setType(types[1])

    def isGlobal(self):
        return self.type == types[1]

    def setPropertyType(self):
        self._setType(types[2])

    def isProperty(self):
        return self.type == types[2]

    def setMethodType(self):
        self._setType(types[3])

    def isMethod(self):
        return self.type == types[3]

    def setClassType(self):
        self._setType(types[4])

    def isClass(self):
        return self.type == types[4]


    def getMethods(self):
        return filter(lambda field: field.isMethod(), self.fields.values())
