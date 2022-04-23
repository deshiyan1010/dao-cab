from datetime import datetime
import hashlib
import json
import requests
from uuid import uuid4
from urllib.parse import urlparse
from trie import Trie

class Blockchain:

    def __init__(self,pubKey,pvtKey):
        self.chain = []
        self.transactions = []
        self.bookings = []
        self.ride_done = []
        self.create_block(proof=1, previous_hash='0')
        self.nodes = set()
        self.pubKey = pubKey
        self.pvtKey = pvtKey
        self.trie = Trie()

    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash,
                 'transactions': self.transactions,
                 'ride_bookings': self.ride_done}

        self.transactions = []
        self.ride_done = []
        return block

    def append_block(self,block):
        self.chain.append(block)


    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(
                str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def mine_block(self):
        previous_block = self.get_previous_block()
        previous_proof = previous_block['proof']
        proof = self.proof_of_work(previous_proof)
        previous_hash = self.hash(previous_block)
        self.add_transaction(self.pubKey, "COINBASE", 1)
        block = self.create_block(proof, previous_hash)
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
        if self.trie.calculate_balance(sender)>=amount:
            self.transactions.append({
                'sender': sender,
                'receiver': receiver,
                'amount': amount
            })
            self.trie.insert_txn(self.transactions[-1])
            return True
        return False

    def add_booking(self, passenger, from_loc, to_loc):
        self.bookings.append({
            'passenger': passenger,
            'from_loc': from_loc,
            'to_loc': to_loc,
            'provider':None,
            'amount':None,
        })
        previous_block = self.get_previous_block()
        return previous_block['index'] + 1




