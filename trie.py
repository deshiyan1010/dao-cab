from rsa import PublicKey
from mcodes import *
import pickle
import os

class Node:
    
    def __init__(self,val):
        self.val = val
        self.childrens = {}

class End:

    def __init__(self):
        self.bid_war = {}
        self.activeRequest = None
        self.activeServicing = None
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
    #     self.load()




    def insert(self, word) -> None:
        res = self.insertWord(word,0,self.master)
        return res


    def search(self, word) -> bool:
        print(word,type(word),"\n\n\n")
        x = self.dfsSearchStrict(word,0,self.master)
        print(x)
        return x 
        


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


        sender = txn_block['sender']

        valid,end = self.search(sender)
        if not valid:
            end = self.insert(sender)
        end.txn[TXN_OUT].append(txn_block)

        valid,end = self.search(txn_block['receiver'])
        if not valid:
            end = self.insert(txn_block['receiver'])
        end.txn[TXN_IN].append(txn_block)


    def insert_ride_request(self,ride_block):
        valid,end = self.search(ride_block['passenger'])
        if not valid:
            end = self.insert(ride_block['passenger'])
        
        end.activeRequest = ride_block

    def assign_provider(self,passenger,provider,amount):


        valid,end = self.search(passenger)
        if not valid:
            end = self.insert(passenger)

        end.activeRequest['provider'] = provider
        end.activeRequest['amount'] = amount

        ride_block = end.activeRequest

        valid,end = self.search(provider)
        if not valid:
            end = self.insert(provider)
        
        end.activeServicing = ride_block

    def ride_completed(self,passenger):
        valid,end = self.search(passenger)
        if not valid:
            end = self.insert(passenger)

        end.rides[RIDES_TAKEN].append(end.activeRequest)
        provider = end.activeRequest['provider']
        ride_block = end.activeRequest
        end.activeRequest = None

        valid,end = self.search(provider)
        if not valid:
            end = self.insert(provider)
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
            'found':False,
            'txin':[],
            'txout':[],
            'ridetaken':[],
            'rideprovided':[],
            'bid_war':None,
            'activeRequest':None,
            'activeServicing':None,
            'pubKey':pubKey
        }

        valid,end = self.search(pubKey)
        if not valid:
            return response

        response['txin'] = end.txn[TXN_IN]
        response['txout'] = end.txn[TXN_OUT]
        response['ridetaken'] = end.rides[RIDES_TAKEN]
        response['rideprovided'] = end.rides[RIDES_PROVIDED]
        response['found'] = True
        response['bid_war'] = end.bid_war
        response['activeRequest'] = end.activeRequest
        response['activeServicing'] = end.activeServicing

        # for i in range(len(response['txin'])):
        #     response['txin'][i]['receiver'] = response['txin'][i]['receiver']
        #     response['txin'][i]['sender'] = response['txin'][i]['sender']

        # for i in range(len(response['txout'])):
        #     response['txout'][i]['receiver'] = response['txout'][i]['receiver']
        #     response['txout'][i]['sender'] = response['txout'][i]['sender']

        # for i in range(len(response['ridetaken'])):
        #     response['ridetaken'][i]['provider'] = response['ridetaken'][i]['provider']
        #     response['ridetaken'][i]['passenger'] = response['ridetaken'][i]['passenger']

        # for i in range(len(response['rideprovided'])):
        #     response['rideprovided'][i]['provider'] = response['rideprovided'][i]['provider']
        #     response['rideprovided'][i]['passenger'] = response['rideprovided'][i]['passenger']


        return response


if __name__=="__main__":
    t = Trie()
    # t.insert("hello")
    print(t.search("hello"))
