from transaction import Transaction
from node import Node
from candidate import Candidate

class CompliantNode(Node):
    def __init__(self, p_graph, p_mallicious, p_txDistribution, numRound):
        self._p_graph = p_graph
        self._p_malicious = p_mallicious
        self._p_txDistribution = p_txDistribution
        self._numRounds = numRound
        self._currentRound = 0
        self._oldRound = 0
        self._followees = []
        self._blacklists = []
        self._consensusTrans = set()
        self._pendingTrans = set()
        return

    def setFollowees(self, followees):
        self._followees = followees
        self._blacklists = [False] * len(followees)
        return

    def setPendingTransaction(self, pendingTransactions):
        self._pendingTrans = pendingTransactions
        self._consensusTrans = pendingTransactions.copy()
        return

    def sendToFollowers(self) -> set:
        Txs = set()
        if self._currentRound == self._numRounds:
            Txs = self._consensusTrans
        elif self._currentRound < self._numRounds:
            Txs.update(self._pendingTrans)
            self._oldRound = self._currentRound
        return Txs
    
    def checkMalicious(self, candidates: set) -> None:
        senders = {c.sender for c in candidates}
        for i, followee in enumerate(self._followees):
            if followee and i not in senders:
                # Node might be functionally dead and never actually broadcast any transactions
                self._blacklists[i] = True

    def receiveFromFollowees(self, candidates: set):
        self._currentRound += 1
        if self._currentRound >= self._numRounds-1:
            return
        if self._oldRound > 0 and self._currentRound > self._oldRound:
            self._pendingTrans.clear()
        self.checkMalicious(candidates)
        
        for c in candidates:
            if c.tx not in self._consensusTrans and not self._blacklists[c.sender]:
                self._consensusTrans.add(c.tx)
                self._pendingTrans.add(c.tx)
        return
