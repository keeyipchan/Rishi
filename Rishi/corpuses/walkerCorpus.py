__author__ = 'Robur'

#base class for all walkers
class WalkerCorpus:
    #will be called at the start of walk
    def prepareToWalk(self,state):
        pass

    #will be called at the beginning of looking of new node
    def enterNode(self,node,state):
        pass

    #will be called at the end of looking of new node
    def exitNode(self,node,state):
        pass

