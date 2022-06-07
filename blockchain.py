from datetime import datetime
import hashlib
import json
import requests
from uuid import uuid4
from urllib.parse import urlparse
from trie import Trie


class Mining:
 
    __shared_state = dict()
 
    def __init__(self):
        self.__dict__ = self.__shared_state
        self.mining = False


class Blockchain:

    def __init__(self,pubKey,pvtKey,gmining):
        self.chain = []
        self.transactions = []
        self.local_txn_hash = ''
        self.booking_open_req = []
        self.booking_on_going = []
        self.booking_fulfilled = []
        genBlock = self.create_block(proof=1, previous_hash='0')
        self.append_block(genBlock)

        self.pubKey = pubKey
        self.pvtKey = pvtKey
        self.trie = Trie()
        self.globalMine = gmining


    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash,
                 'transactions': self.transactions,
                 'ride_bookings': self.booking_fulfilled}

        return block

    def append_block(self,block):
        self.transactions = []
        self.chain.append(block)


    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while self.globalMine.mining==True and check_proof is False:
            hash_operation = hashlib.sha256(
                str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        
        if self.globalMine.mining:
            return new_proof
        else:
            return -1

    def mine_block(self):

        previous_block = self.get_previous_block()
        previous_proof = previous_block['proof']
        previous_hash = self.hash(previous_block)
        

        proof = self.proof_of_work(previous_proof)
        
        if self.globalMine.mining==False:
            return None,None

        

        coinbasetxn = {
            'sender': "COINBASE",
            'receiver': self.pubKey,
            'amount': 1
            }

        self.transactions.append(coinbasetxn)

        block = self.create_block(None, previous_hash)
        block['proof'] = proof   
        response = {'message': 'Congratulations, you just mined a block!',
                    'index': block['index'],
                    'transactions': block['transactions'],
                    'timestamp': block['timestamp'],
                    'proof': block['proof'],
                    'previous_hash': block['previous_hash']}

        return response,block

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block["proof"]
            proof = block["proof"]
            hash_operation = hashlib.sha256(
                str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != "0000":
                return False
            previous_block = block
            block_index += 1
        return True

    def add_transaction(self, sender, receiver, amount):
        block = {
                'sender': sender,
                'receiver': receiver,
                'amount': amount
                }
        if sender!="COINBASE" and self.trie.calculate_balance(sender)>=amount:
            self.local_txn_hash += self.hash(block)
            self.local_txn_hash = hashlib.sha256(self.local_txn_hash.encode()).hexdigest()
            self.transactions.append(block)
            return True
        return False

    def add_booking(self, passenger, from_loc, to_loc):
        self.booking_open_req.append({
            'passenger': passenger,
            'from_loc': from_loc,
            'to_loc': to_loc,
            'provider':None,
            'amount':None,
        })



    def get_balance(self,pubKey):
        return self.trie.calculate_balance(pubKey)

    # def clear_mempool(self):
    #     print("see i am clearing")
    #     self.transactions=[]
    #     print(self.transactions)
    #     print("i cleared mempools!!")
    #     return True 

