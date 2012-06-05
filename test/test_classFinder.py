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

    def test04FindPropertiesInConstructor(self):
        self.walk('''
        b=function (add) {this.x=1}
        b.prototype.c = function () {}
        ''')

        self.classFinder.analyzeClassNodes()
        clazz = self.classFinder.getClass('b')
        self.assertTrue(clazz.getObject('x').isProperty())