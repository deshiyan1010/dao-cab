
from consesus import Consesus
from ecc import EllipticCurveCryptography
from blockchain import Blockchain

class EndPoint:
    def __init__(self,ip,port,publicKey,hashedMessage):
        self.ip = ip 
        self.port = port
        self.publicKey = publicKey
        self.hashedMessage = hashedMessage

    def verify(self):
        return EllipticCurveCryptography.verify(*self.publicKey,*self.hashedMessage)
    
    def __hash__(self) -> int:
        return super.__hash__(str(self.ip)+str(self.port))

class Connection:

    def __init__(self):
        self.nodes = set()
        self.blockchain = Blockchain()
        self.consesus = Consesus()

    def connect(self,):
        pass

    def addNode(self,):
        pass

    def leave(self,):
        pass
    
    def removeNode(self,):
        pass

    def request_block_verification(self,):
        pass
    
    def broadcast_block(self,):
        pass

    def get_chain(self,):
        pass

    def request_neighbour_for_neighbours(self,):
        pass

    def block_addition(self,):
        pass

    def broadcast_message(self,):
        pass

    def add_transaction(self,):
        pass

    def book_ride(self,):
        pass
    
    