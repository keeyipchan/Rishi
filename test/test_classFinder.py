import unittest
from Object import Object
from Rishi.corpuses.classFinder import ClassFinder
from Rishi.parser.JSParser import Parser
from Rishi.walker import Walker

__author__ = 'Robur'


class test_ClassFinder(unittest.TestCase):
    classes = {}
    glob = None

    def walk(self, src):
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

        self.assertEqual(len(self.classFinder.classes), 2)
        self.assertEqual(self.classFinder.getClass('c').name, 'c')
        self.assertTrue(self.classFinder.getClass('c').isClass())
        self.assertEqual(self.classFinder.getClass('c').parent.name, '<global>')
        self.assertEqual(self.classFinder.getClass('a.b').parent.name, 'a')

    def test02PrototypeBasedMethodExtractor(self):
        self.walk('''
        a.b.prototype.d = function (asd) {}
        ''')

        method = self.classFinder.getClass('a.b').getObject('d')
        self.assertIsNotNone(method)
        self.assertTrue(method.isMethod())
        self.assertEqual(method.node.arguments[0], 'asd')

    def test03assingFunctionToObject(self):
        self.walk('''
        b=function (add) {}
        b.prototype.c = function () {}
        ''')

        clazz = self.classFinder.getClass('b')
        self.assertIsNotNone(clazz)
        self.assertEqual(clazz.node.arguments[0], 'add')

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
        b=function (add) {this.x=123}
        ''')

        clazz = self.classFinder.getClass('b')
        self.assertIsNotNone(clazz)
        self.assertTrue(clazz.getObject('x').isProperty())
        self.assertEqual(len(clazz.fields), 1)

    def test06FindPropertiesInMethod(self):
        self.walk('''
        b=function (add) {}
        b.prototype.c = function () {
            this.y.d=123
        }
        ''')

        clazz = self.classFinder.getClass('b')
        self.assertTrue(clazz.getObject('y').isProperty())
        self.assertEqual(len(clazz.fields), 2)

    def test07CreatePropertyConstructorLink(self):
        self.walk('''
        a.b=function () {
            this.x = new e()
        }
        b=function () { this.y =1}
        a.c = function () {
            this.y = new a.b();
            this.u = new b()
            this.u = new a.b()
        }
        ''')

        self.assertEqual(len(self.classFinder.classes), 3)
        clazz = self.classFinder.getClass('a.c')
        self.assertEqual(len(clazz.links), 2)


    def test08testReturningToGlobalScope(self):
        self.walk('''
            a=function () {};

            a.prototype.c = function () {
             function asd () {
             }
            }
        ''')

        self.assertEqual(self.classFinder.scope, self.classFinder.globalObj)

    def test09testCorrectThisParse(self):
        self.walk('''
            a=function () {
                this.c()
                this.e.t()
            };

            a.prototype.b = function () {
                this.d()
            }
        ''')

        clazz = self.classFinder.getClass('a')
        self.assertEqual(len(clazz.fields), 4)
        self.assertTrue(clazz.getObject('c').isMethod())
        self.assertTrue(clazz.getObject('d').isMethod())
        self.assertTrue(clazz.getObject('b').isMethod())
        self.assertTrue(clazz.getObject('e').isProperty())



