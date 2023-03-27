import copy

from utxo import UTXO, UTXOPool
from transaction import Transaction
from crypto import Crypto
import decimal

class TxHandler:
    """
    Creates a public ledger whose current UTXOPool (collection of unspent transaction outputs) is {@code pool}.
    """
    def __init__(self, pool: UTXOPool):
        self._utxoPool =  pool
        return

    """
    @return true if:
    (1) all outputs claimed by {@code tx} are in the current UTXO pool, 
    (2) the signatures on each input of {@code tx} are valid, 
    (3) no UTXO is claimed multiple times by {@code tx},
    (4) all of {@code tx}s output values are non-negative, and
    (5) the sum of {@code tx}s input values is greater than or equal to the sum of its output
        values; and false otherwise.
    """
    def isValidTx(self, tx: Transaction) -> bool:
        sumInput = 0
        sumOutput = 0
        usedUTXO = dict()
        
        for i in range(tx.numInputs()):
            input_ = tx.getInput(i)
            outputIndex = input_.outputIndex
            prevTxHash = input_.prevTxHash
            signature = input_.signature
            
            utxo = UTXO(prevTxHash, outputIndex)
            
            # check rule (1): all outputs claimed by tx are in current UTXO pool
            if not self._utxoPool.contains(utxo):
                return False
            # check rule (2): the signatures on each input of tx are valid
            output = self._utxoPool.getTxOutput(utxo)
            message = tx.getRawDataToSign(i)
            if not Crypto.verifySignature(output.address, message, signature):
                return False
            # check rule (3): no UTXO is claimed multiple times by tx
            if utxo in usedUTXO:
                return False
            usedUTXO[utxo] = True

            sumInput += output.value
        
        # check rule (4): all of tx output values are non-negative
        for i in range(tx.numOutputs()):
            output = tx.getOutput(i)
            if output.value < 0:
                return False
            sumOutput += output.value
        
        # check rule (5): the sum of tx input values is greater than or equal to the sum of its output values
        if sumInput < sumOutput:
            return False
        
        return True


    """
    Handles each epoch by receiving an unordered array of proposed transactions, checking each
    transaction for correctness, returning a mutually valid array of accepted transactions, and
    updating the current UTXO pool as appropriate.
    """
    def handleTxs(self, txs):
        validTxs = []
        for t in txs:
            if self.isValidTx(t):
                validTxs.append(t)
                
                # remove utxo
                for input_ in t.inputs:
                    outputIndex = input_.outputIndex
                    prevTxHash = input_.prevTxHash
                    utxo = UTXO(prevTxHash, outputIndex)
                    self._utxoPool.removeUTXO(utxo)
                
                # add new utxo
                hash_ = t.hash
                for i in range(t.numOutputs()):
                    utxo = UTXO(hash_, i)
                    self._utxoPool.addUTXO(utxo, t.getOutput(i))
        
        return validTxs
