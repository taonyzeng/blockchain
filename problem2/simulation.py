from numpy import random, full

from compliant_node import CompliantNode
from malicious_node import MaliciousNode
from transaction import Transaction
from candidate import Candidate

class Simulation:

    def __init__(self, numNodes: int, p_graph: float, p_mal: float, p_txD: float, numR: int):
        self._numNodes = numNodes
        self._pGraph = p_graph
        self._pMalicious = p_mal
        self._pTxDistribution = p_txD
        self._numRounds = numR

    @property
    def numNodes(self):
        """The number of nodes in graph

        :return: integer
        """
        return self._numNodes

    @property
    def p_graph(self):
        """The pairwise connectivity probability of the random graph

        :return: float e.g. {.1, .2, .3}
        """
        return self._pGraph

    @property
    def p_malicious(self):
        """The probability that a node will be set to be malicious

        :return: float  e.g {.15, .30, .45}
        """
        return self._pMalicious

    @property
    def p_txDistribution(self):
        """The probability that each of the initial valid transactions
        will be communicated

        :return: float e.g. {.01, .05, .10}
        """
        return self._pTxDistribution

    @property
    def numRounds(self):
        """The number of rounds in the simulation

        :return: integer e.g. {10, 20}
        """
        return self._numRounds

    def main(self):

        # Step 1
        nodes = []
        compliants = []

        for i in range(self.numNodes):
            if random.rand() < self.p_malicious:
                nodes.append(MaliciousNode(self.p_graph, self.p_malicious, self.p_txDistribution, self.numRounds))
            else:
                node = CompliantNode(self.p_graph, self.p_malicious, self.p_txDistribution, self.numRounds)
                nodes.append(node)
                compliants.append(node)

        # Step 2
        followees = full((self.numNodes, self.numNodes), False)
        for i in range(self.numNodes):
            for j in range(self.numNodes):
                if i == j:
                    continue
                if random.rand() < self.p_graph:
                    followees[i][j] = True

        for i in range(self.numNodes):
            nodes[i].setFollowees(followees[i])

        # Step 3
        numTx = 500
        validTxIds = {i for i in range(numTx)}

        possibleConsensus = set()
        for i in range(self.numNodes):
            pendingTransactions = set()
            for txID in validTxIds:
                if random.rand() < self.p_txDistribution:
                    pendingTransactions.add(Transaction(txID))
            nodes[i].setPendingTransaction(pendingTransactions)
            if isinstance(nodes[i], CompliantNode):
                possibleConsensus |= pendingTransactions

        # Step 4
        for _round in range(self.numRounds):
            allProposals = dict()

            for i in range(self.numNodes):
                proposals = nodes[i].sendToFollowers()

                for tx in proposals:
                    if tx.id not in validTxIds:
                        continue

                    for j in range(self.numNodes):
                        if not followees[j][i]:
                            continue

                        if j not in allProposals:
                            allProposals[j] = set()

                        candidate = Candidate(tx, i)
                        allProposals[j].add(candidate)

            for i in range(self.numNodes):
                if i in allProposals:
                    nodes[i].receiveFromFollowees(allProposals[i])

        # Step 5
        groups = dict()
        for i in range(self.numNodes):
            if isinstance(nodes[i], CompliantNode):
                ids = [tx.id for tx in nodes[i].sendToFollowers()]
                ids.sort()
                ids = tuple(ids)
                if ids not in groups:
                    groups[ids] = []
                groups[ids].append(i)

        for txs, nodes in groups.items():
            print("Node group: %d/%d" % (len(nodes), len(compliants)))
            print(nodes)
            print("Consensus: %d/%d" % (len(txs), len(possibleConsensus)))
            print(txs)
            print()

if __name__ == "__main__":
    s = Simulation(numNodes = 100, p_graph = 0.1, p_mal = 0.3, p_txD = 0.01, numR = 10)
    s.main()
