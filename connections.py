
# from crypt import methods
from flask_cors import CORS

from numpy import block
from consesus import Consesus
from ecc import EllipticCurveCryptography
from blockchain import Blockchain,Mining
from hashQ import Queue

from urllib import response
from flask import Flask,request, signals_available
from flask_classful import FlaskView,route
from flask import jsonify
import argparse
import requests
from flask import jsonify, make_response
import atexit

import hashlib
from pprint import pprint
import json

import pickle

import os

from functools import wraps

# import logging

# log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)


parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", help = "Port")
args = parser.parse_args()

app = Flask(__name__)
CORS(app)
host='0.0.0.0'
port=args.port

ecc = EllipticCurveCryptography()


mining = Mining()

def retriveState():
    if str(port) not in set(os.listdir()):
        pubx,puby,pvt = ecc.generate_ecc_pair()
        pvt = hex(pvt)
        comp = ecc.compress_pubKey(pubx,puby)
        blockchain = Blockchain(comp,pvt,mining)
        return blockchain,comp,pvt

    file = open(os.path.join(str(port),"blockchain"), 'rb')
    blockchain = pickle.load(file)
    file.close()
    blockchain.globalMine = mining
    return blockchain,blockchain.pubKey,blockchain.pvtKey

nodes = set()

blockchain,comp,pvt = retriveState()
consesus = Consesus(blockchain)

print(comp,pvt)
queue = Queue(100)

def save(func):
    @wraps(func)
    def inner(*args, **kwargs):
        x = func(*args, **kwargs)
        if str(port) not in os.listdir():
            os.mkdir(str(port))
        file = open(os.path.join(str(port),"blockchain"), 'wb')
        pickle.dump(blockchain,file)
        file.close()
        return x 
    return inner

class Connection(FlaskView):
    route_base = '/'

    def __init__(self,starter_node=None):
        if starter_node!=None:
            req = jsonify({
                "ip":starter_node.split(":")[0],
                "port":starter_node.split(":")[1]
                })
            requests.post(self.combine(host,port,"connect"),json=req)

        atexit.register(self.purge)

    @save
    def block_addition(self,block):
        consesus.add_block(block)


    def broadcast_message_get(self,url,data):
        response = {}
        for endpoint in nodes:
            temp = requests.get(self.combine(*endpoint,url),json=data).json()
            response[":".join(endpoint)] = temp
        return response

    def broadcast_message_post(self,url,data):
        
        hashed = hashlib.sha1(json.dumps(data).encode('utf-8')).hexdigest()
    
        if queue.search(hashed):
            return
        
        queue.insert(hashed)
        for endpoint in nodes:
            requests.post(self.combine(*endpoint,url),json=data).json()


    def combine(self,ip,port,path):
        return "http://"+ip+":"+port+"/"+path
    
    def leave(self,):
        req = {"ip":host,"port":port}
        self.broadcast_message_post('purge',req)
        exit(0)

    def request_block_verification(self,block):
        if consesus.validate_block(block):
            return True
        return False

    def broadcasted(self,data):
        hashed = hashlib.sha1(json.dumps(data).encode('utf-8')).hexdigest()
        return queue.search(hashed)


    @route('/getkey',methods=["GET"])
    def getKey(self,):
        return jsonify({"pub":comp,"pvt":pvt}),200

    @route('/connect',methods=['POST'])
    def connect(self):
        data = {
            "ip":host,
            "port":port
            }
        
        req = request.get_json()
        nodeIP = req['ip']
        nodePort = req['port']
        req_obj = requests.post(self.combine(nodeIP,nodePort,"addNode"),json=data)

        if req_obj.status_code!=200:
            return jsonify({'message':'failed'}),400
    
        nodes.add((nodeIP,nodePort))
        return jsonify({'message':'connected'}),200


    @route('/neighbors',methods=['GET'])
    def getNeighbors(self,):
        return jsonify({'neigh':list(nodes)}),200


    @route('/addNode',methods=['POST'])
    def addNode(self,):
        
        req = request.get_json()
        nodes.add((req['ip'],req['port']))
        return jsonify({'message':'added'}),200


    @route('/purge',methods=['POST'])
    def purge(self,):
        req = request.get_json()
        
        if (req['ip'],req['port']) not in nodes:
            resp = jsonify({"message":"Request purge node not in node set"})
            return resp, 404
        
        nodes.pop((req['ip'],req['port']))
        return jsonify({}), 200
    
    
    @route('/blockbroadcast',methods=['POST'])
    @save
    def broadcast_block(self,):
        req = request.get_json()
        block = req["block"]

        if not self.broadcasted(req):
            if self.request_block_verification(block):
                mining.mining = False
                self.broadcast_message_post('blockbroadcast',req)
                self.block_addition(block)
                return jsonify({}),200
            else:
                message = "ALERT: Invalid block. This block will not be broadcasted."
                return jsonify({"message":message}), 400

        return jsonify({"message":"repeat request"}),200

    @route('/getdata',methods=['GET'])
    def get_data(self,):
        response = {
            'chain': blockchain.chain, 
            'chainlength': len(blockchain.chain),
            'mempool_txn':blockchain.transactions
            }
        return make_response(jsonify(response), 200)

    @route('/rnfn',methods=['GET'])
    def request_neighbours_for_neighbor(self,):
        response = self.broadcast_message_get('neighbors',{})

        for _,js in response.items():
            for nip,nport in js['neigh']:
                nodes.add((nip,nport))
        nodes.remove((host,port))
        return jsonify(response), 200

    
    @route('/mine',methods=["POST"])
    def mine(self):

        mining.mining = True
        response,block = blockchain.mine_block()
        if response==None:
            return jsonify({"message":"mining was out raced"}),408
        # consesus.add_block(block)
        mining.mining = False

        # self.broadcast_message_post('blockbroadcast',{"block":block})
        requests.post(self.combine(host,port,"blockbroadcast"),json={"block":block})
        return jsonify(response),200
    
    @route('/balance',methods=["GET"])
    def get_balance(self):

        req = request.get_json()

        bal = blockchain.get_balance(req["pub"])
        return jsonify({"bal":bal}), 200
    

    @route('/broadcasttxn',methods=['POST'])
    @save
    def broadcast_transaction(self,):
        txnblock = request.get_json()

        if ecc.verify(txnblock['sender'],txnblock['signed_hash'],txnblock['signature_r'],txnblock['signature_s']) and not self.broadcasted(txnblock) and blockchain.get_balance(txnblock['sender'])>=txnblock['amount']:
            blockchain.add_transaction(txnblock)
            self.broadcast_message_post('broadcasttxn',txnblock)
            return jsonify({}),200
        else:
            return jsonify({"message":"Signature verification failed OR repeate broadcast OR insufficient balance"}),400


    @route('/addtxn',methods=['POST'])
    @save
    def add_transaction(self,):

        #params public key, signed hash, reciever and amount   REFER ecc.py FOR GENERATING SIGNATURES AND VERIFICATION  
        #https://cryptobook.nakov.com/digital-signatures/ecdsa-sign-verify-messages to know now ecc signing and verification works
        #step1 : validate signed hash and public key
        #step2 : get the end node
        #step3 : calculate balance
        #step4 : if valid add to mempool
        #step5 : broadcast_message

        req = request.get_json()
        block = blockchain.create_txn_block(req)
        reqObj = requests.post(self.combine(host,port,'broadcasttxn'),json=block)
        return jsonify(reqObj.json()),reqObj.status_code



    @route('/bookride',methods=['POST'])
    @save
    def book_ride(self):
        
        #params passenger, signed hash, pick_loc,drop_loc
        #step1 : validate signed hash and public key
        #step2:  broadcast_message

        req = request.get_json()
        print("----------------",ecc.verify(req['passenger'],req['signed_hash'],req['signature_r'],req['signature_s']), not self.broadcasted(req))
        if ecc.verify(req['passenger'],req['signed_hash'],req['signature_r'],req['signature_s']) and not self.broadcasted(req):
            print("ADDED")
            print("BRGIS")
            # pprint(blockchain.gis.__dict__)
            blockchain.add_booking(req['passenger'],req['pick_loc'], req['drop_loc'])
            self.broadcast_message_post('bookride',req)
            print("BRGIS")
            pprint(blockchain.gis.__dict__)
            return jsonify({}),200
        else:
            return jsonify({"message":"Signature verification failed OR repeate broadcast"}),400


    @route('/listride',methods=['GET'])
    @save
    def list_ride(self):
        r = request.get_json()
        print(r,"\n\n\n\n")
        ride_list = []

        for record in blockchain.get_ride_requests(r['k'],r['lat'],r['long']):
            rec = {}
            rec['pick'] =(record[0],record[1])
            rec['pubKey'] = record[2]
            request_block = blockchain.get_block(record[2])[1].activeRequest
            rec['drop'] = (request_block['to_loc'])
            ride_list.append(rec)
        return jsonify({"list":ride_list}),200
    
    @route('/getservicereq',methods=['GET'])
    def get_assigned_ride(self):
        r = request.get_json()
        found,block = blockchain.get_block(r['pubKey'])
        if not found:
            return jsonify({'job':None}),200
        return jsonify({'job':block.activeServicing}),200


    @route('/endride',methods=['POST'])
    @save
    def end_ride(self):
        req = request.get_json()
        print(req)
        print(ecc.verify(req['passenger'],req['signed_hash'],req['signature_r'],req['signature_s']), not self.broadcasted(req))

        if ecc.verify(req['passenger'],req['signed_hash'],req['signature_r'],req['signature_s']) and not self.broadcasted(req):
            print("ENDGIS")
            pprint(blockchain.gis.__dict__)
            blockchain.end_ride(req['passenger'])
            print("ENDGIS")
            pprint(blockchain.gis.__dict__)
            self.broadcast_message_post('endride',req)
            return jsonify({}),200
        else:
            return jsonify({"message":"Signature verification failed OR repeate broadcast"}),400

    @route('/bidride',methods=['POST'])
    @save
    def bid_ride(self):
        req = request.get_json()
        if not self.broadcasted(req):
            blockchain.bid(req['passenger'],req['provider'],req['bid'])
            self.broadcast_message_post('bidride',req)
            return jsonify({}),200
        return jsonify({}),400


    @route('/selbidride',methods=['POST'])
    @save
    def sel_bid_ride(self):
        req = request.get_json()

        print(blockchain.gis.__dict__)
        if ecc.verify(req['passenger'],req['signed_hash'],req['signature_r'],req['signature_s']) and not self.broadcasted(req):
            print("SELGIS")
            pprint(blockchain.gis.__dict__)
            blockchain.select_bid(req['passenger'],req['provider'])
            print("SELGIS")
            pprint(blockchain.gis.__dict__)
            self.broadcast_message_post('selbidride',req)
            return jsonify({}),200
        else:
            return jsonify({"message":"Signature verification failed OR repeate broadcast"}),400


    @route('/bidlist',methods=['GET'])
    @save
    def bid_list(self):
        req = request.get_json()
        return jsonify(blockchain.trie.retrieve_data(req['passenger'])['bid_war']),200





    @route('/getsigs',methods=["GET"])   
    def getsig(self,):
        req = request.get_json()
        return jsonify(ecc.sign(req['pvt'],None)),200

    @route('/genpubpvt',methods=["GET"])   
    def getPubPvt(self,):
        pubx,puby,pvt = ecc.generate_ecc_pair()
        pvt = hex(pvt)
        comp = ecc.compress_pubKey(pubx,puby)
        return jsonify({"pub":comp,"pvt":pvt}),200


    @route('/explore',methods=["GET"])
    def explore(self):
        pubKey = request.get_json()["pubKey"]
        return jsonify(blockchain.trie.retrieve_data(pubKey)),200

    @route('/requestredirect',methods=["POST"])   
    def redirect(self):
        requestJson = request.get_json()
        reqType = requestJson["reqtype"].lower()
        req = requestJson['req']

        requestJson.pop('reqtype')
        requestJson.pop('req')

        if reqType=="post":
            return jsonify(requests.post(self.combine(host,port,req),json=requestJson).json()),200
        else: 
            return jsonify(requests.get(self.combine(host,port,req),json=requestJson).json()),200


    @route('/meta',methods=["GET"])   
    def metadata(self):
        chain = blockchain.chain
        mempool = blockchain.transactions

        txn_count = 0
        supply = 0
        for i in range(len(chain)):
            txn_count+=len(chain[i]['transactions'])
            for t in chain[i]['transactions']:
                supply += t['amount']



        meta = {
            'latest_block':chain[-1]['index'],
            'txn_count':txn_count,
            'pen_txn':mempool,
            'total_supply':supply,
            'latest_txn':chain[-1]['transactions'],
            'chain':chain
        }


        return jsonify({'meta':meta}),200


Connection.register(app,route_base = '/')
app.run(host=host,port=port,debug=True)