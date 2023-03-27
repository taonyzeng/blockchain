class Node:
    def setFollowees(self, followees):
        return NotImplemented

    def setPendingTransaction(self, pendingTransactions):
        return NotImplemented

    def sendToFollowers(self) -> set:
        return NotImplemented

    def receiveFromFollowees(self, candidates: set):
        return NotImplemented
