from mcodes import *

class Node:
    
    def __init__(self,val):
        self.val = val
        self.childrens = {}

class End:

    def __init__(self):
        self.rides = {
            RIDES_TAKEN:[],
            RIDES_PROVIDED:[]
        }
        self.txn = {
            TXN_IN:[],
            TXN_OUT:[]
        }

class Trie:

    def __init__(self):
        self.master = Node(-1)
        
    def insert(self, word: str) -> None:
        return self.insertWord(word,0,self.master)

    def search(self, word: str) -> bool:
        return self.dfsSearchStrict(word,0,self.master)

    def insertWord(self,word,ptr,node):
        if ptr<len(word):
            if word[ptr] not in node.childrens:
                node.childrens[word[ptr]] = Node(word[ptr])
            return self.insertWord(word,ptr+1,node.childrens[word[ptr]])
        else:
            node.childrens[-1] = End()
            return node.childrens[-1]

    def dfsSearchStrict(self,word,ptr,node):
        if ptr<len(word):
            if word[ptr] in node.childrens:
                return self.dfsSearchStrict(word,ptr+1,node.childrens[word[ptr]])
            else:
                return False,None

        if -1 in node.childrens:
            return True,node.childrens[-1]

        return False,None

    def insert_txn(self,txn_block):
        valid,end = self.search(txn_block['sender'])
        if not valid:
            end = self.insert(txn_block['sender'])
        end.txn[TXN_OUT].append(txn_block)

        valid,end = self.search(txn_block['receiver'])
        if not valid:
            end = self.insert(txn_block['receiver'])
        end.txn[TXN_IN].append(txn_block)

    def insert_ride(self,ride_block):
        valid,end = self.search(ride_block['passenger'])
        if not valid:
            end = self.insert(ride_block['passenger'])
        end.rides[RIDES_TAKEN].append(ride_block)

        valid,end = self.search(ride_block['provider'])
        if not valid:
            end = self.insert(ride_block['provider'])
        end.rides[RIDES_PROVIDED].append(ride_block)

    def calculate_balance(self,pubKey):
        valid,end = self.search(pubKey)
        if not valid:
            return 0
        inAmt = 0
        outAmt = 0
        for tx in end.txn[TXN_IN]:
            inAmt += tx['amount']
        for tx in end.txn[TXN_OUT]:
            outAmt += tx['amount']
        return inAmt-outAmt

    def retrieve_data(self,pubKey):

        response = {
            'txin':[],
            'txout':[],
            'ridetaken':[],
            'rideprovided':[]
        }

        valid,end = self.search(pubKey)
        if not valid:
            return response