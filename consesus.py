
from blockchain import Blockchain
import hashlib

class Consesus:
    def __init__(self,blockchain:Blockchain):
        self.blockchain = blockchain

    def checktxn(self,block):
        local_txn_hash = self.blockchain.local_txn_hash
        block_txn_hash = ''

        for b in block['transactions']:
            if b['sender']!="COINBASE":
                block_txn_hash+=self.blockchain.hash(b)
                block_txn_hash = hashlib.sha256(block_txn_hash.encode()).hexdigest()
        print(block_txn_hash,local_txn_hash)
        if local_txn_hash==block_txn_hash:
            return True 
        return False

    def validate_block(self,block):
        #ind txn existance check missing
        new_proof = block['proof']
        previous_proof = self.blockchain.get_previous_block()['proof']
        hash_operation = hashlib.sha256(
            str(new_proof**2 - previous_proof**2).encode()).hexdigest()
        if hash_operation[:4] == '0000' and block['transactions'][-1]['sender']=="COINBASE" and block['transactions'][-1]['amount']==1 and self.checktxn(block):
            return True
        return False


    def add_block(self,block):
        for txn in block['transactions']:
            self.blockchain.trie.insert_txn(txn)
        self.blockchain.append_block(block)
