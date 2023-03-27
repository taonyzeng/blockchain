import unittest
import copy
import decimal

from crypto import Crypto
from transaction import Transaction
from utxo import UTXO, UTXOPool
from txhandler import TxHandler
from testutil import generateKeyPair, createSignature, getSha256Hash

class TestTxHandler(unittest.TestCase):
    def setUp(self):
        # Create a UTXOPool with some initial unspent outputs
        self.utxoPool = UTXOPool()
        self.pair = generateKeyPair()

    def test_isValidTx(self):
        # Create a valid transaction
        tx1 = Transaction()

        tx1.addOutput(10, self.pair)
        tx1.finalize()
        utxo = UTXO(tx1.hash, 0)
        self.utxoPool.addUTXO(utxo, tx1.getOutput(0))

        tx2 = Transaction()
        tx2.addOutput(5, self.pair)
        tx2.finalize()
        utxo2 = UTXO(tx2.hash, 0)
        self.utxoPool.addUTXO(utxo2, tx2.getOutput(0))
        
        handler = TxHandler(self.utxoPool)

        tx = Transaction()
        tx.addInput(tx1.hash, 0)
        tx.addOutput(7.50, self.pair)

        input = tx.getInput(0)
        signature = createSignature(tx.getRawDataToSign(0), self.pair)

        input.addSignature(signature)

        tx.finalize()
        self.assertTrue(len(tx.getRawTx()) > 0)

        self.assertTrue(handler.isValidTx(tx))

    def test_isValidTxMissingUtxo(self):
        tx1 = Transaction()

        tx1.addOutput(10, self.pair)
        tx1.finalize()
        # utxo = UTXO(tx1.hash, 0)
        # self.utxoPool.addUTXO(utxo, tx1.getOutput(0))

        handler = TxHandler(self.utxoPool)

        tx = Transaction()
        tx.addInput(tx1.hash, 0)
        tx.addOutput(7.50, self.pair)

        input = tx.getInput(0)
        signature = createSignature(tx.getRawDataToSign(0), self.pair)

        input.addSignature(signature)

        tx.finalize()
        self.assertTrue(len(tx.getRawTx()) > 0)

        self.assertFalse(handler.isValidTx(tx))

    def test_isValidTxInvalidSignature(self):
        tx1 = Transaction()

        tx1.addOutput(10, self.pair)
        tx1.finalize()
        utxo = UTXO(tx1.hash, 0)
        self.utxoPool.addUTXO(utxo, tx1.getOutput(0))

        handler = TxHandler(self.utxoPool)

        tx = Transaction()
        tx.addInput(tx1.hash, 0)
        tx.addOutput(7.50, self.pair)

        input = tx.getInput(0)
        signature = createSignature(tx.getRawDataToSign(0), generateKeyPair())

        input.addSignature(signature)

        tx.finalize()
        self.assertTrue(len(tx.getRawTx()) > 0)

        self.assertFalse(handler.isValidTx(tx))

    def test_isValidTxMultipleUtxoClaim(self):
        tx1 = Transaction()

        tx1.addOutput(10, self.pair)
        tx1.finalize()
        utxo = UTXO(tx1.hash, 0)
        self.utxoPool.addUTXO(utxo, tx1.getOutput(0))

        handler = TxHandler(self.utxoPool)

        tx = Transaction()
        tx.addInput(tx1.hash, 0)
        tx.addInput(tx1.hash, 0)
        tx.addOutput(7.50, self.pair)

        input = tx.getInput(0)
        signature = createSignature(tx.getRawDataToSign(0), self.pair)

        input.addSignature(signature)

        input = tx.getInput(1)
        signature = createSignature(tx.getRawDataToSign(1), self.pair)

        input.addSignature(signature)

        tx.finalize()
        self.assertTrue(len(tx.getRawTx()) > 0)

        self.assertFalse(handler.isValidTx(tx))

    def test_isValidTxNegativeOutput(self):
        tx1 = Transaction()

        tx1.addOutput(10, self.pair)
        tx1.finalize()
        utxo = UTXO(tx1.hash, 0)
        self.utxoPool.addUTXO(utxo, tx1.getOutput(0))

        handler = TxHandler(self.utxoPool)

        tx = Transaction()
        tx.addInput(tx1.hash, 0)
        tx.addOutput(-7.50, self.pair)

        input = tx.getInput(0)
        signature = createSignature(tx.getRawDataToSign(0), self.pair)

        input.addSignature(signature)

        tx.finalize()
        self.assertTrue(len(tx.getRawTx()) > 0)

        self.assertFalse(handler.isValidTx(tx))

    def test_isValidTxExceedsInput(self):
        tx1 = Transaction()

        tx1.addOutput(10, self.pair)
        tx1.finalize()
        utxo = UTXO(tx1.hash, 0)
        self.utxoPool.addUTXO(utxo, tx1.getOutput(0))

        handler = TxHandler(self.utxoPool)

        tx = Transaction()
        tx.addInput(tx1.hash, 0)
        tx.addOutput(17.50, self.pair)
        tx.addOutput(10.00, self.pair)

        input = tx.getInput(0)
        signature = createSignature(tx.getRawDataToSign(0), self.pair)

        input.addSignature(signature)

        tx.finalize()
        self.assertTrue(len(tx.getRawTx()) > 0)

        self.assertFalse(handler.isValidTx(tx))

    def test_handleTxs(self):
        tx1 = Transaction()

        tx1.addOutput(10, self.pair)
        tx1.finalize()
        utxo = UTXO(tx1.hash, 0)
        self.utxoPool.addUTXO(utxo, tx1.getOutput(0))

        tx2 = Transaction()
        tx2.addOutput(5, self.pair)
        tx2.finalize()
        utxo = UTXO(tx2.hash, 0)
        self.utxoPool.addUTXO(utxo, tx2.getOutput(0))

        handler = TxHandler(self.utxoPool)

        tx3 = Transaction()
        tx3.addInput(tx1.hash, 0)
        tx3.addOutput(7.50, self.pair)

        input = tx3.getInput(0)
        signature = createSignature(tx3.getRawDataToSign(0), self.pair)
        input.addSignature(signature)
        tx3.finalize()

        tx4 = Transaction()
        tx4.addInput(tx2.hash, 0)
        tx4.addOutput(10, self.pair)

        input = tx4.getInput(0)
        signature = createSignature(tx4.getRawDataToSign(0), self.pair)
        input.addSignature(signature)
        tx4.finalize()

        possibleTxs = [tx3, tx4]

        validTxs = handler.handleTxs(possibleTxs)
        self.assertEqual(1, len(validTxs))
        self.assertEqual(tx3, validTxs[0])

if __name__ == '__main__':
    unittest.main()
