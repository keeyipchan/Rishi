from Rishi.corpuses.walkerCorpus import WalkerCorpus
from Rishi.parser import AST

__author__ = 'Robur'

class ScopeTracer(WalkerCorpus):

    def prepareToWalk(self, state):
        state['scopes'] = ['Global']

    def enterNode(self, node, state):
        if isinstance(node, AST.FunctionBody):
            print("NEW SCOPE---->")
            state['scopes'].append(node)

    def exitNode(self, node, state):
        if isinstance(node, AST.FunctionBody):
            print("SCOPE END<----")
            state['scopes'].pop()
