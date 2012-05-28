from Rishi.corpuses.walkerCorpus import WalkerCorpus
from Rishi.parser import AST
#from Rishi.scope import Scope

__author__ = 'Robur'

class ScopeTracer(WalkerCorpus):

    def prepareToWalk(self, state, root):
#        state['root scope'] = Scope(root, None)
        state['scope'] = state['root scope']

    def enterNode(self, node, state):
        if isinstance(node, AST.FunctionBody):
            print("NEW SCOPE---->")
            state['scope'] = state['scope'].newScope(node)


    def exitNode(self, node, state):
        if isinstance(node, AST.FunctionBody):
            print("SCOPE END<----")
            state['scope'] = state['scope'].parent
