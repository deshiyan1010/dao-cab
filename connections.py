
from crypt import methods
from consesus import Consesus
from ecc import EllipticCurveCryptography
from blockchain import Blockchain

from urllib import response
from flask import Flask,request
from flask_classful import FlaskView,route
from flask import jsonify

import requests



app = Flask(__name__)
host='0.0.0.0'
port=5000

class Connection(FlaskView):
    route_base = '/'

    def __init__(self,starter_node):
        pubx,puby,pvt = EllipticCurveCryptography.generate_ecc_pair()
        self.nodes = set()
        self.blockchain = Blockchain(pubx,puby,pvt)
        self.consesus = Consesus(self.blockchain)
        self.connect(*starter_node.split(":"))

    def combine(self,ip,port,path):
        return ip+":"+port+"/"+path

    def connect(self,nodeIP,nodePort):
        req = jsonify({
            "ip":host,
            "port":port
            })
        
        req_obj = requests.post(self.combine(nodeIP,nodePort,"addNode"),data=req)
        
        if req_obj.status_code!=200:
            print("Problem connecting")
            exit(0)
    
        print("Connected")
        
        self.node.add(tuple(nodeIP,nodePort))
        

    @route('/addNode',methods=['POST'])
    def addNode(self,):
        req = request.get_json()
        self.nodes.add((req['ip'],req['port']))
        return jsonify({}),200

    def leave(self,):
        req = jsonify({"ip":host,"port":port})
        self.broadcast_message('purge',req)
        exit(0)


    @route('/purge',methods=['POST'])
    def purge(self,):
        req = request.get_json()
        
        if (req['ip'],req['port']) not in self.nodes:
            resp = jsonify({"message":"Request purge node not in node set"})
            return resp, 404
        
        self.nodes.pop((req['ip'],req['port']))
        return jsonify({}), 200
        
    
    def request_block_verification(self,block):
        if self.consesus.validate_block(block):
            return True
        return False
        
    
    @route('/blockbroadcast',methods=['POST'])
    def broadcast_block(self,):
        req = request.get_json()
        block = req["block"]

        if self.request_block_verification(block):
            self.broadcast_message('blockbroadcast',req)
            self.block_addition(block)
            return jsonify({}),200
        else:
            return jsonify({"message":"ALERT: Invalid block. This block will not be broadcasted."}), 400


    @route('/getchain',methods=['GET'])
    def get_chain(self,):
        response = {'chain': self.blockchain.chain, 'length': len(self.blockchain.chain)}
        return jsonify(response), 200

    def request_neighbours_for_neighbor(self,):
        response = {'neighbors': self.nodes}
        return jsonify(response), 200

    def block_addition(self,block):
        self.consesus.add_block(block)

    def broadcast_message(self,url,data):
        for endpoint in self.nodes:
            requests.post(self.combine(*endpoint,url),data=data)

    
    def add_transaction(self,):
        #params public key, signed hash, reciever and amount
        #step1 : validate signed hash and public key
        #step2 : get the end node
        #step3 : calculate balance
        #step4 : if valid add to blockchain
        #step5 : add the data to the txn_out in the end node
        #step6 : add the data in to the txn_receiver
        #step7: broadcast_message
        pass

    def book_ride(self,passenger,signed_hash,pick_loc,drop_loc):
        #params passenger, signed hash, pick_loc,drop_loc
        #step1 : validate signed hash and public key
        #step2:  broadcast_message
        
        pass
    

Connection.register(app,route_base = '/')
app.run()