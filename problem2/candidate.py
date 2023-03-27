from transaction import Transaction

class Candidate:
    def __init__(self, tx: Transaction, sender: int):
        self._tx = tx
        self._sender = sender

    @property
    def tx(self):
        return self._tx

    @property
    def sender(self):
        return self._sender

    def __eq__(self, other):
        if not isinstance(other, Candidate):
            return NotImplemented
        return self._tx == other._tx and self._sender == other._sender

    def __hash__(self):
        return hash((self._tx, self._sender))
