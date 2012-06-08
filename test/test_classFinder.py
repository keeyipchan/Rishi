import unittest
from Rishi.corpuses.classFinder import ClassFinder, Object
from Rishi.parser.JSParser import Parser
from Rishi.walker import Walker

__author__ = 'Robur'


class test_ClassFinder(unittest.TestCase):
    classes = {}
    glob  = None

    def walk(self,src):
        parser = Parser()
        parser.setSrc(src)
        self.walker = Walker()
        self.walker.setAst(parser.buildAST())
        self.glob = Object('<global>')
        self.classFinder = ClassFinder(self.glob, self.classes)
        self.walker.addWatcher(self.classFinder)
        self.walker.walk()

    def setUp(self):
        super().setUp()

    def test01PrototypeBasedObjectExtractor(self):
        self.walk('''
        a.b.prototype.d = function () {}
        c.prototype.d = function () {}
        b.c = function() {}
        ''')

        self.assertEqual(len(self.classFinder.classes),2)
        self.assertEqual(self.classFinder.getClass('c').name,'c')
        self.assertTrue(self.classFinder.getClass('c').isClass())
        self.assertEqual(self.classFinder.getClass('c').parent.name,'<global>')
        self.assertEqual(self.classFinder.getClass('a.b').parent.name,'a')

    def test02PrototypeBasedMethodExtractor(self):
        self.walk('''
        a.b.prototype.d = function (asd) {}
        ''')

        method = self.classFinder.getClass('a.b').getObject('d')
        self.assertIsNotNone(method)
        self.assertTrue(method.isMethod())
        self.assertEqual(method.node.arguments[0],'asd')

    def test03assingFunctionToObject(self):
        self.walk('''
        b=function (add) {}
        b.prototype.c = function () {}
        ''')

        clazz = self.classFinder.getClass('b')
        self.assertIsNotNone(clazz)
        self.assertEqual(clazz.node.arguments[0],'add')

    def test04TestMethodAndConstructorGlobalScope(self):
        self.walk('''
        b=function (add) {}
        b.prototype.c = function () {}
        ''')

        clazz = self.classFinder.getClass('b')
        self.assertEqual(clazz.outerScope, self.classFinder.globalObj)
        self.assertEqual(clazz.getObject('c').outerScope, self.classFinder.globalObj)


    def test05FindPropertiesInConstructor(self):
        self.walk('''
        b=function (add) {this.x=this.y.g}
        ''')

        clazz = self.classFinder.getClass('b')
        self.assertIsNotNone(clazz)
        self.assertTrue(clazz.getObject('x').isProperty())
        self.assertTrue(clazz.getObject('y').isProperty())
        self.assertEqual(len(clazz.fields),2)

    def test06FindPropertiesInMethod(self):
        self.walk('''
        b=function (add) {}
        b.prototype.c = function () {
            this.y.d=this.x
        }
        ''')

        clazz = self.classFinder.getClass('b')
        self.assertTrue(clazz.getObject('x').isProperty())
        self.assertTrue(clazz.getObject('y').isProperty())
        self.assertEqual(len(clazz.fields),3)

    def test06CreatePropertyConstructorLink(self):
        self.walk('''
        a.b=function () { this.x =1}
        b=function () { this.y =1}
        a.c = function () {
            this.y = new a.b();
            this.u = new b()
            this.u = new a.b()
        }
        ''')

        self.assertEqual(len(self.classFinder.classes),3)
        clazz = self.classFinder.getClass('a.c')
        self.assertEqual(len(clazz.links),2)




