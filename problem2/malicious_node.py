from transaction import Transaction
from node import Node
from candidate import Candidate
from numpy import random

class MaliciousNode(Node):
    def __init__(self, p_graph, p_mallicious, p_txDistribution, numRound):
        pass
    # YOU MAY TRY TO WRITE YOUR OWN CODE FOR MALICIOUS NODES WITH ARBITRARY BEHAVIOR TO TEST YOUR SOLUTION 
        

    def setFollowees(self, follow):
        pass
    # YOU MAY TRY TO WRITE YOUR OWN CODE FOR MALICIOUS NODES WITH ARBITRARY BEHAVIOR TO TEST YOUR SOLUTION


    def setPendingTransaction(self, pendingTransactions):
        pass
    # YOU MAY TRY TO WRITE YOUR OWN CODE FOR MALICIOUS NODES WITH ARBITRARY BEHAVIOR TO TEST YOUR SOLUTION

    def sendToFollowers(self) -> set:
        return set()
    # YOU MAY TRY TO WRITE YOUR OWN CODE FOR MALICIOUS NODES WITH ARBITRARY BEHAVIOR TO TEST YOUR SOLUTION

    def receiveFromFollowees(self, candidates: set):
        pass
    # YOU MAY TRY TO WRITE YOUR OWN CODE FOR MALICIOUS NODES WITH ARBITRARY BEHAVIOR TO TEST YOUR SOLUTION
