
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
        self.consesus = Consesus(self.blockchain)

    def connect(self,node_addr):
        pass

    def addNode(self,):
        pass

    def leave(self,):
        pass
    
    def removeNode(self,):
        #action to leave request
        pass

    def request_block_verification(self,):
        pass
    
    def broadcast_block(self,):
        pass

    def get_chain(self,):
        pass

    def request_neighbours_for_neighbour(self,):
        #list of neighbouring addreses
        pass

    def block_addition(self,):
        pass

    def broadcast_message(self,):
        pass
    
    def add_transaction(self,):
        #params public key, signed hash, reciever and amount
        #step1 : validate signed hash and public key
        #step2 : get the end node
        #step3 : calculate balance
        #step4 : if valid add to blockchain
        #step5 : add the data to the txn_out in the end node
        #step6 : add the data in to the txn_receiver
        #step7: broadcast_message
        pass

    def book_ride(self,passenger,signed_hash,pick_loc,drop_loc):
        #params passenger, signed hash, pick_loc,drop_loc
        #step1 : validate signed hash and public key
        #step2:  broadcast_message
        
        pass
    
#check token balance while accepting bid