
from crypt import methods
from consesus import Consesus
from ecc import EllipticCurveCryptography
from blockchain import Blockchain,Mining
from hashQ import Queue

from urllib import response
from flask import Flask,request
from flask_classful import FlaskView,route
from flask import jsonify
import argparse
import requests
import atexit

import hashlib

import json

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", help = "Port")
args = parser.parse_args()

app = Flask(__name__)
host='127.0.0.1'
port=args.port

ecc = EllipticCurveCryptography()
pubx,puby,pvt = ecc.generate_ecc_pair()
comp = ecc.compress_pubKey(pubx,puby)
nodes = set()
blockchain = Blockchain(comp,pvt)
consesus = Consesus(blockchain)

mining = Mining()
queue = Queue(100)

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


    def combine(self,ip,port,path):
        return "http://"+ip+":"+port+"/"+path
    
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

    def leave(self,):
        req = jsonify({"ip":host,"port":port})
        self.broadcast_message_post('purge',req)
        exit(0)


    @route('/purge',methods=['POST'])
    def purge(self,):
        req = request.get_json()
        
        if (req['ip'],req['port']) not in nodes:
            resp = jsonify({"message":"Request purge node not in node set"})
            return resp, 404
        
        nodes.pop((req['ip'],req['port']))
        return jsonify({}), 200
        
    
    def request_block_verification(self,block):
        if consesus.validate_block(block):
            return True
        return False
        
    
    @route('/blockbroadcast',methods=['POST'])
    def broadcast_block(self,):
        req = request.get_json()
        block = req["block"]

        if self.request_block_verification(block):
            mining.mining = False
            self.broadcast_message_post('blockbroadcast',req)
            self.block_addition(block)
            return jsonify({}),200
        else:
            return jsonify({"message":"ALERT: Invalid block. This block will not be broadcasted."}), 400


    @route('/getdata',methods=['GET'])
    def get_data(self,):
        response = {
            'chain': blockchain.chain, 
            'chainlength': len(blockchain.chain),
            'mempool_txn':blockchain.transactions
            }
        return jsonify(response), 200

    @route('/rnfn',methods=['GET'])
    def request_neighbours_for_neighbor(self,):
        response = self.broadcast_message_get('neighbors',{})

        for _,js in response.items():
            for nip,nport in js['neigh']:
                nodes.add((nip,nport))
        nodes.remove((host,port))
        return jsonify(response), 200

    def block_addition(self,block):
        consesus.add_block(block)

    def broadcast_message_get(self,url,data):
        response = {}
        for endpoint in nodes:
            temp = requests.get(self.combine(*endpoint,url),json=data).json()
            response[":".join(endpoint)] = temp
        print(response)
        return response

    def broadcast_message_post(self,url,data):
        hashed = hashlib.sha1(json.dumps(data).encode('utf-8')).hexdigest()
        if queue.search(hashed):
            return
        queue.insert(hashed)
        for endpoint in nodes:
            requests.post(self.combine(*endpoint,url),json=data).json()

    @route('/mine',methods=["POST"])
    def mine(self):
        mining.mining = True
        response,block = blockchain.mine_block()
        if response==None:
            return jsonify({"message":"mining was out raced"}),408

        mining.mining = False
        self.broadcast_message_post('blockbroadcast',block)
        return response,200

    @route('/addtxn',methods=['GET'])
    def add_transaction(self,):
        #params public key, signed hash, reciever and amount
        #step1 : validate signed hash and public key
        #step2 : get the end node
        #step3 : calculate balance
        #step4 : if valid add to blockchain
        #step5 : add the data to the txn_out in the end node
        #step6 : add the data in to the txn_receiver
        #step7 : broadcast_message

        req = request.get_json()
        if ecc.verify(req['sender'],req['signed_hash'],req['signature_pair']):
            blockchain.add_transaction(req['sender'],req['receiver'], req['amount'])
            self.broadcast_message_post('addtxn',req)
            return jsonify({}),200
        else:
            return jsonify({"message":"Signature verification failed"}),400

        pass
    
    @route('/bookride',methods=['GET'])
    def book_ride(self):
        
        #params passenger, signed hash, pick_loc,drop_loc
        #step1 : validate signed hash and public key
        #step2:  broadcast_message

        req = request.get_json()
        if ecc.verify(req['passenger'],req['signed_hash'],req['signature_pair']):
            blockchain.add_booking(req['passenger'],req['pick_loc'], req['drop_loc'])
            return jsonify({}),200
        else:
            return jsonify({"message":"Signature verification failed"}),400
    

Connection.register(app,route_base = '/')
app.run(host=host,port=port,debug=True)