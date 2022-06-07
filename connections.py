
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






parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", help = "Port")
args = parser.parse_args()

app = Flask(__name__)
host='127.0.0.1'
port=args.port

ecc = EllipticCurveCryptography()


mining = Mining()

def retriveState():
    if str(port) not in set(os.listdir()):
        pubx,puby,pvt = ecc.generate_ecc_pair()
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


queue = Queue(100)

def save(func):
    @wraps(func)
    def inner(*args, **kwargs):
        x = func(*args, **kwargs)
        # if str(port) not in os.listdir():
        #     os.mkdir(str(port))
        # file = open(os.path.join(str(port),"blockchain"), 'wb')
        # pickle.dump(blockchain,file)
        # file.close()
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
            print(requests.post(self.combine(*endpoint,url),json=data).json())


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
        return jsonify({"pub":comp,"pvt":pvt,"pubh":hex(comp),"pvth":hex(pvt)}),200

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
                print("SELF: ",message)
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
        if isinstance(req["pub"],str):
            req["pub"] = int(req["pub"],16)
        
        bal = blockchain.get_balance(req["pub"])
        return jsonify({"bal":bal}), 200

    
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
        print(ecc.verify(req['sender'],req['signed_hash'],req['signature_r'],req['signature_s']))
        if ecc.verify(req['sender'],req['signed_hash'],req['signature_r'],req['signature_s']) and not self.broadcasted(req) and blockchain.get_balance(req['sender'])>=req['amount']:
            blockchain.add_transaction(req['sender'],req['receiver'], req['amount'])
        
            self.broadcast_message_post('addtxn',req)
            return jsonify({}),200
        else:
            return jsonify({"message":"Signature verification failed OR repeate broadcast OR insufficient balance"}),400

    
    @route('/bookride',methods=['GET'])
    @save
    def book_ride(self):
        
        #params passenger, signed hash, pick_loc,drop_loc
        #step1 : validate signed hash and public key
        #step2:  broadcast_message

        req = request.get_json()
        if ecc.verify(req['sender'],req['signed_hash'],req['signature_r'],req['signature_s']) and not self.broadcasted(req):
            blockchain.add_booking(req['passenger'],req['pick_loc'], req['drop_loc'])
            self.broadcast_message_post('bookride',req)
            return jsonify({}),200
        else:
            return jsonify({"message":"Signature verification failed OR repeate broadcast"}),400


    @route('/listride',methods=['GET'])
    @save
    def list_ride(self):
        r = request.get_json()
        return jsonify({"list":blockchain.get_ride_requests(r['k'],r['lat'],r['long'])}),200
    


    @route('/endride',methods=['POST'])
    @save
    def end_ride(self):
        req = request.get_json()
        if ecc.verify(req['sender'],req['signed_hash'],req['signature_r'],req['signature_s']) and not self.broadcasted(req):
            blockchain.end_ride(req['passenger'])
            self.broadcast_message_post('endride',req)
            return jsonify({}),200
        else:
            return jsonify({"message":"Signature verification failed OR repeate broadcast"}),400

    @route('/bidride',methods=['POST'])
    @save
    def bid_ride(self):
        req = request.get_json()
        blockchain.bid(req['passenger'],req['provider'],req['bid'])
        return jsonify({}),200

    @route('/selbidride',methods=['POST'])
    @save
    def sel_bid_ride(self):
        req = request.get_json()
        if ecc.verify(req['sender'],req['signed_hash'],req['signature_r'],req['signature_s']) and not self.broadcasted(req):
            blockchain.select_bid(req['passenger'],req['provider'])
            self.broadcast_message_post('selbidride',req)
            return jsonify({}),200
        else:
            return jsonify({"message":"Signature verification failed OR repeate broadcast"}),400


    @route('/getsigs',methods=["GET"])   
    def getsig(self,):
        req = request.get_json()
        return jsonify(ecc.sign(req['pvt'],None)),200


    @route('/requestredirect',methods=["POST"])   
    def redirect(self):
        requestJson = request.get_json()

        if requestJson["reqtype"].lower()=="post":
            return jsonify(requests.post(self.combine(host,port,requestJson['req']),json=requestJson).json()),200
        else: 
            return jsonify(requests.get(self.combine(host,port,requestJson['req']),json=requestJson).json()),200





Connection.register(app,route_base = '/')
app.run(host=host,port=port,debug=True)