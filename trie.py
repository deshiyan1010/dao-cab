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

    # def load(self,file="trie"):
    #     if file not in set(os.listdir()):
    #         return
    #     self.master = pickle.load(open(os.path.join(str(port),"blockchain"), 'wb')).master


    def is_hex(self,s):
        try:
            int(s, 16)
            return True
        except:
            return False

    def get_hex(self,word):
        # print(word,type(word))

        if word=="COINBASE":
            return word

        if isinstance(word,str) and word[:2]!="0x":
            word = hex(int(word))
        elif isinstance(word,int):
            word = hex(word)
        return word



    def insert(self, word) -> None:
        word = self.get_hex(word)
        res = self.insertWord(word,0,self.master)
        return res


    def search(self, word) -> bool:
        word = self.get_hex(word)
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
        if txn_block['sender']!="COINBASE":
            sender = self.get_hex(txn_block['sender'])
        else:
            sender = "COINBASE"

        valid,end = self.search(sender)
        if not valid:
            end = self.insert(sender)
        end.txn[TXN_OUT].append(txn_block)

        valid,end = self.search(self.get_hex(txn_block['receiver']))
        if not valid:
            end = self.insert(self.get_hex(txn_block['receiver']))
        end.txn[TXN_IN].append(txn_block)


    def insert_ride_request(self,ride_block):
        valid,end = self.search(self.get_hex(ride_block['passenger']))
        if not valid:
            end = self.insert(self.get_hex(ride_block['passenger']))
        
        end.activeRequest = ride_block

    def assign_provider(self,passenger,provider,amount):
        passenger = self.get_hex(passenger)
        provider = self.get_hex(provider)

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
        passenger = self.get_hex(passenger)
        valid,end = self.search(passenger)
        if not valid:
            end = self.insert(passenger)

        end.rides[RIDES_TAKEN].append(end.activeRequest)
        provider = self.get_hex(end.activeRequest['provider'])
        ride_block = end.activeRequest
        end.activeRequest = None

        valid,end = self.search(provider)
        if not valid:
            end = self.insert(provider)
        end.rides[RIDES_PROVIDED].append(ride_block)


    def calculate_balance(self,pubKey):
        pubKey = self.get_hex(pubKey)
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
        
        pubKey = self.get_hex(pubKey)
        print("\n"*10,pubKey)
        response = {
            'found':False,
            'txin':[],
            'txout':[],
            'ridetaken':[],
            'rideprovided':[]
        }

        valid,end = self.search(pubKey)
        if not valid:
            return response

        response['txin'] = end.txn[TXN_IN]
        response['txout'] = end.txn[TXN_OUT]
        response['ridetaken'] = end.rides[RIDES_TAKEN]
        response['rideprovided'] = end.rides[RIDES_PROVIDED]
        response['found'] = True
        

        for i in range(len(response['txin'])):
            response['txin'][i]['receiver'] = self.handled_hex(response['txin'][i]['receiver'])
            response['txin'][i]['sender'] = self.handled_hex(response['txin'][i]['sender'])

        for i in range(len(response['txout'])):
            response['txout'][i]['receiver'] = self.handled_hex(response['txout'][i]['receiver'])
            response['txout'][i]['sender'] = self.handled_hex(response['txout'][i]['sender'])

        for i in range(len(response['ridetaken'])):
            response['ridetaken'][i]['provider'] = self.handled_hex(response['ridetaken'][i]['provider'])
            response['ridetaken'][i]['passenger'] = self.handled_hex(response['ridetaken'][i]['passenger'])

        for i in range(len(response['rideprovided'])):
            response['rideprovided'][i]['provider'] = self.handled_hex(response['rideprovided'][i]['provider'])
            response['rideprovided'][i]['passenger'] = self.handled_hex(response['rideprovided'][i]['passenger'])


        return response


    def handled_hex(self,word):
        try:
            return hex(word)
        except:
            return word

if __name__=="__main__":
    t = Trie()
    # t.insert("hello")
    print(t.search("hello"))
