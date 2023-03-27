class Transaction:
	
    def __init__(self, id: int):
        self._id = id

    @property
    def id(self):
    	return self._id
    
    def __eq__(self, other):
        if isinstance(other, Transaction):
            return self.id == other.id
        else:
            return NotImplemented

    def __hash__(self):
        return hash(self.id)
