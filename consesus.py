
from blockchain import Blockchain
import hashlib

class Consesus:
    def __init__(self,blockchain:Blockchain):
        self.blockchain = blockchain

    def validate_block(self,block):
        new_proof = block['proof']
        previous_proof = self.blockchain.get_previous_block()['proof']
        hash_operation = hashlib.sha256(
            str(new_proof**2 - previous_proof**2).encode()).hexdigest()
        if hash_operation[:4] == '0000':
            return True
        return False


    def add_block(self,block):
        self.blockchain.append_block(block)
