import unittest
from Rishi.corpuses.classFinder import ClassFinder
from Rishi.parser.JSParser import Parser
from Rishi.walker import Walker

__author__ = 'Robur'


class test_ClassFinder(unittest.TestCase):

    def walk(self,src):
        parser = Parser()
        parser.setSrc(src)
        self.walker = Walker()
        self.walker.setAst(parser.buildAST())
        self.classFinder = ClassFinder()
        self.walker.addWatcher(self.classFinder)
        self.walker.walk()

    def setUp(self):
        super().setUp()

    def test01PrototypeBasedObjectExtractor(self):
        self.walk('''
        a.prototype.d = function () {}
        b.c = function() {}
        ''')

        self.assertEqual(len(self.classFinder.classes),1)
        self.assertEqual(self.classFinder.getClass('a').name,'a')

    def test02PrototypeBasedObjectExtractor(self):
        self.walk('''
        a.prototype.d = function () {}
        b.c = function() {}
        ''')

        self.assertEqual(len(self.classFinder.classes),1)
        self.assertEqual(self.classFinder.getClass('a').name,'a')



