from datetime import datetime
import hashlib
import json
from click import pass_context
import requests
from uuid import uuid4
from urllib.parse import urlparse
from mcodes import ACTIVE_REQ_ON, NO_ACTIVE_REQ, RIDES_PROVIDED, RIDES_TAKEN, SEARCH_FAILED, SUCCESS
from trie import Trie
from gis import GIS

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

        self.booking_fulfilled = []
        genBlock = self.create_block(proof=1, previous_hash='0')
        self.append_block(genBlock)

        self.pubKey = pubKey
        self.pvtKey = pvtKey
        self.trie = Trie()
        self.globalMine = gmining
        self.gis = GIS(1)

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
        self.booking_fulfilled = []
        self.local_txn_hash = ''
        self.chain.append(block)

    def get_block(self,pubKey):
        found,block = self.trie.search(pubKey)
        return found,block

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
            'amount': 1,
            'timestamp':str(datetime.now())
            }

        self.transactions.append(coinbasetxn)

        block = self.create_block(None, previous_hash)
        block['proof'] = proof   
        response = {'message': 'Congratulations, you just mined a block!',
                    'index': block['index'],
                    'transactions': block['transactions'],
                    'timestamp': block['timestamp'],
                    'proof': block['proof'],
                    'previous_hash': block['previous_hash'],
                    'ride_bookings':block['ride_bookings']}

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

    def add_transaction(self, block):

        if block['sender']!="COINBASE" and self.trie.calculate_balance(block['sender'])>=block['amount']:
            self.local_txn_hash += self.hash(block)
            self.local_txn_hash = hashlib.sha256(self.local_txn_hash.encode()).hexdigest()
            self.transactions.append(block)
            return True
        return False


    def create_txn_block(self,req):
        req['timestamp'] = str(datetime.now())
        return req


    def add_booking(self, passenger, from_loc, to_loc):
        
        found,block = self.trie.search(passenger)

        if not found:
            block = self.trie.insert(passenger)
            found,block = self.trie.search(passenger)

        if block.activeRequest:
            return ACTIVE_REQ_ON

        ride_recipt = {
            'passenger': passenger,
            'from_loc': from_loc,
            'to_loc': to_loc,
            'provider':None,
            'amount':None,
            'timestamp': str(datetime.now()),
        }
        block.activeRequest = ride_recipt

        self.gis.addToBucket(*from_loc,passenger,ride_recipt)

        return SUCCESS


    def end_ride(self,passenger):

        found,block = self.trie.search(passenger)

        if not found:
            return SEARCH_FAILED
        
        
        if not block.activeRequest:
            return NO_ACTIVE_REQ
        
        data = block.activeRequest
        block.activeRequest = None 

        self.booking_fulfilled.append(data)

        block.rides[RIDES_TAKEN].append(data)

        provider = data['provider']
        found,block = self.trie.search(provider)

        block.activeServicing = None 
        block.rides[RIDES_PROVIDED].append(data)

        return SUCCESS


    def bid(self,passenger,provider,bid):

        found,block = self.trie.search(passenger)

        if not found:
            block = self.trie.insert(passenger)
        
        print("\n\n\n\n\nBID")
        print(block.bid_war)
        if not block.activeRequest:
            return NO_ACTIVE_REQ

        block.bid_war[provider]=bid
        print("\n\n\n\n\nBID")
        print(block.bid_war)

    def select_bid(self,passenger,provider):

        found,block = self.trie.search(passenger)

        if not found:
            return SEARCH_FAILED
        
        if not block.activeRequest:
            return NO_ACTIVE_REQ

        print("\n\n\n\n\nBID")
        print(block.bid_war)
        bid = block.bid_war[provider]
        block.bid_war = {}
        print("\n\n\n\n\nBID")
        self.gis.remove(passenger)

        block.activeRequest['provider'] = provider
        block.activeRequest['amount'] = bid 
        data = block.activeRequest

        found,block = self.trie.search(provider)

        if not found:
            block = self.trie.insert(provider)

        block.activeServicing = data 

        return SUCCESS


    def get_ride_requests(self,k,lat,long):
        return self.gis.get_radius(k,lat,long)



    def get_balance(self,pubKey):
        return self.trie.calculate_balance(pubKey)

