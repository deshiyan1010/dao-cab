from time import sleep
import requests
import json
from pprint import pprint
import sys 
sys.path.append('..')
from ecc import EllipticCurveCryptography
from pprint import pprint
from datetime import datetime
import time


def combine(ip,port,path):
    return "http://"+ip+":"+port+"/"+path

host = "127.0.0.1"
# "http://"+"127.0.0.1"+":"+"5000"+"/"+getdata
p1 = "5001"
p2 = "5002"
p3 = "5003"



# Connecting the nodes p2 and p3 to p1 and checking p1's neighbors

data = {
    "ip":host,
    "port":p2,
    "time":time.time()
    }
print(1,requests.post(combine(host,p1,'connect'),json=data).json())
print(2,requests.get(combine(host,p1,'neighbors')).json())


data = {
    "ip":host,
    "port":p3,
    "time":time.time()
    }
print(3,requests.post(combine(host,p2,'connect'),json=data).json())
print(4,requests.get(combine(host,p2,'neighbors')).json())



keysP1 = requests.get(combine(host,p1,'getkey')).json()
keysP2 = requests.get(combine(host,p2,'getkey')).json()
keysP3 = requests.get(combine(host,p3,'getkey')).json()
privateKeyP1 = keysP1["pvt"]
publicKeyP1 = keysP1["pub"]
privateKeyP2 = keysP2["pvt"]
publicKeyP2 = keysP2["pub"]
publicKeyP3 = keysP3["pub"]
privateKeyP3 = keysP3["pvt"]

print(5,publicKeyP1,publicKeyP2,publicKeyP3)

jsonx = {"pubKey":publicKeyP1,"time":time.time()}
print(35, "Rider")
pprint(requests.get(combine(host,p1,'explore'), json=jsonx).json())

jsonx = {"pubKey":publicKeyP2,"time":time.time()}
print(36, "Provider")
pprint(requests.get(combine(host,p1,'explore'), json=jsonx).json())






ecc = EllipticCurveCryptography()
signed_object = ecc.sign(privateKeyP1)
signature_r = signed_object['r']
signature_s = signed_object['s']



transData={
    "passenger":publicKeyP1,   # Why public key?, as we are doing internal hashing of the public key, so we can use the public key
    "pick_loc":(0.1,0.1),
    "drop_loc":(0.2,0.1),
    "signed_hash":None,
    "signature_r":signature_r,
    "signature_s":signature_s,
    "time":time.time()
}

print(6,requests.post(combine(host,p1,'bookride'),json=transData).json())


jsonx = {'k':1,'lat':0.10001,'long':0.1005,"time":time.time()}
print("lISR",requests.get(combine(host,p3,'listride'), json=jsonx).json())

#AFTER RIDE REQUEST SUBMISSION
#IN P1
jsonx = {"pubKey":publicKeyP1,"time":time.time()}
print(7, "Rider")
print(requests.get(combine(host,p1,'explore'), json=jsonx).json()['activeRequest'])

#IN P2
jsonx = {"pubKey":publicKeyP1,"time":time.time()}
print(8, "Rider")
print(requests.get(combine(host,p2,'explore'), json=jsonx).json()['activeRequest'])

#IN P3
jsonx = {"pubKey":publicKeyP1,"time":time.time()}
print(9, "Rider")
print(requests.get(combine(host,p3,'explore'), json=jsonx).json()['activeRequest'])



#Getting list

jsonx = {'k':1,'lat':0.10001,'long':0.1005,"time":time.time()}
print(10,requests.get(combine(host,p3,'listride'), json=jsonx).json())



#Bidding
jsonx = {'passenger':publicKeyP1,'provider':publicKeyP2,'bid':1,"time":time.time()}
print(11,requests.post(combine(host,p3,'bidride'), json=jsonx).json())

print("Bid placed")
print(12,requests.get(combine(host,p1,'bidlist'), json=jsonx).json())
print(13,requests.get(combine(host,p2,'bidlist'), json=jsonx).json())
print(14,requests.get(combine(host,p3,'bidlist'), json=jsonx).json())



jsonx = {'passenger':publicKeyP1,'provider':publicKeyP3,'bid':1,"time":time.time()}
print(15,requests.post(combine(host,p3,'bidride'), json=jsonx).json())

print("Bid placed")
print(16,requests.get(combine(host,p1,'bidlist'), json=jsonx).json())
print(17,requests.get(combine(host,p2,'bidlist'), json=jsonx).json())
print(18,requests.get(combine(host,p3,'bidlist'), json=jsonx).json())



#Selecting bid
transData={
    "passenger":publicKeyP1,  
    "provider":publicKeyP2,
    "signed_hash":None,
    "signature_r":signature_r,
    "signature_s":signature_s,
    "time":time.time()
}
print(19,requests.post(combine(host,p3,'selbidride'), json=transData).json())

print("Bid placed")
print("19 1",requests.get(combine(host,p1,'bidlist'), json=jsonx).json())
print("19 2",requests.get(combine(host,p2,'bidlist'), json=jsonx).json())
print("19 3",requests.get(combine(host,p3,'bidlist'), json=jsonx).json())



jsonx = {"pubKey":publicKeyP1,"time":time.time()}
print(20, "Rider")
print(requests.get(combine(host,p1,'explore'), json=jsonx).json()['activeRequest'])

jsonx = {"pubKey":publicKeyP1,"time":time.time()}
print(21, "Rider")
print(requests.get(combine(host,p1,'explore'), json=jsonx).json()['activeRequest'])


#IN P2
jsonx = {"pubKey":publicKeyP1,"time":time.time()}
print(22, "Rider")
print(requests.get(combine(host,p2,'explore'), json=jsonx).json()['activeRequest'])

#IN P3
jsonx = {"pubKey":publicKeyP1,"time":time.time()}
print(23, "Rider")
print(requests.get(combine(host,p3,'explore'), json=jsonx).json()['activeRequest'])

jsonx = {'k':1,'lat':0.10001,'long':0.1005,"time":time.time()}
print(24,requests.get(combine(host,p3,'listride'), json=jsonx).json())

# End ride


transData={
    "passenger":publicKeyP1,  
    "provider":publicKeyP2,
    "signed_hash":None,
    "signature_r":signature_r,
    "signature_s":signature_s,
    "time":time.time()
}
print(25,requests.post(combine(host,p3,'endride'), json=transData).json())

#IN P1
jsonx = {"pubKey":publicKeyP1,"time":time.time()}
print(26, "Rider")
print(requests.get(combine(host,p1,'explore'), json=jsonx).json()['activeRequest'])

#IN P2
jsonx = {"pubKey":publicKeyP1,"time":time.time()}
print(27, "Rider")
print(requests.get(combine(host,p2,'explore'), json=jsonx).json()['activeRequest'])

#IN P3
jsonx = {"pubKey":publicKeyP1,"time":time.time()}
print(28, "Rider")
print(requests.get(combine(host,p3,'explore'), json=jsonx).json()['activeRequest'])


#AFTER RIDE END
#IN P1
jsonx = {"pubKey":publicKeyP1,"time":time.time()}
print(29, "Rider")
pprint(requests.get(combine(host,p1,'explore'), json=jsonx).json()['ridetaken'])

jsonx = {"pubKey":publicKeyP2,"time":time.time()}
print(30, "Provider")
pprint(requests.get(combine(host,p1,'explore'), json=jsonx).json()['rideprovided'])


#IN P2
jsonx = {"pubKey":publicKeyP1,"time":time.time()}
print(31, "Rider")
pprint(requests.get(combine(host,p2,'explore'), json=jsonx).json()['ridetaken'])

jsonx = {"pubKey":publicKeyP2,"time":time.time()}
print(32, "Provider")
pprint(requests.get(combine(host,p2,'explore'), json=jsonx).json()['rideprovided'])


#IN P3
jsonx = {"pubKey":publicKeyP1,"time":time.time()}
print(33, "Rider")
pprint(requests.get(combine(host,p3,'explore'), json=jsonx).json()['ridetaken'])

jsonx = {"pubKey":publicKeyP2,"time":time.time()}
print(34, "Provider")
pprint(requests.get(combine(host,p3,'explore'), json=jsonx).json()['rideprovided'])


jsonx = {"pubKey":publicKeyP1,"time":time.time()}
print(35, "Rider")
pprint(requests.get(combine(host,p1,'explore'), json=jsonx).json())

jsonx = {"pubKey":publicKeyP2,"time":time.time()}
print(36, "Provider")
pprint(requests.get(combine(host,p1,'explore'), json=jsonx).json())


# 327732053144230409430711419899576270243849593603494877335522421623534199527687 
# 327730911841986681097836592843987417287867806353322131929635691254694657601006 
# 222450721913100064538976071099491672195376128944214984608165340672728410908986