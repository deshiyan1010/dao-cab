from base64 import b32encode
from time import sleep
import requests
import json
from pprint import pprint
import sys 
sys.path.append('..')
from ecc import EllipticCurveCryptography



def combine(ip,port,path):
    return "http://"+ip+":"+port+"/"+path

host = "0.0.0.0"
# "http://"+"127.0.0.1"+":"+"5000"+"/"+getdata
p1 = "5001"
p2 = "5002"
p3 = "5003"

resip = "0x254dd50c8c59434bb0cd3d7dd4cb513c2c768221472080ee57fe118858d5a6767"

# Connecting the nodes p2 and p3 to p1 and checking p1's neighbors

data = {
    "ip":host,
    "port":p2
    }
print(1,requests.post(combine(host,p1,'connect'),json=data).json())
print(2,requests.get(combine(host,p1,'neighbors')).json())


data = {
    "ip":host,
    "port":p3
    }
print(3,requests.post(combine(host,p2,'connect'),json=data).json())
print(4,requests.get(combine(host,p2,'neighbors')).json())

# mining on p1

print(5,requests.post(combine(host,p1,'mine'),json={}).json())

# print(requests.post(combine(host,p2,'mine'),json={}).json())


# Adding transaction from p1 to p2
keysP1 = requests.get(combine(host,p1,'getkey')).json()
keysP2 = requests.get(combine(host,p2,'getkey')).json()
keysP3 = requests.get(combine(host,p3,'getkey')).json()
privateKeyP1 = keysP1["pvt"]
publicKeyP1 = keysP1["pub"]
privateKeyP2 = keysP2["pvt"]
publicKeyP2 = keysP2["pub"]
publicKeyP3 = keysP3["pub"]
privateKeyP3 = keysP3["pvt"]

signed_object = requests.get(combine(host,p1,'getsigs'),json={"pvt":privateKeyP1}).json()
signature_r = signed_object['r']
signature_s = signed_object['s']


balData={
    "pub":publicKeyP1,
}
b1 = requests.get(combine(host,p1,'balance'), json=balData).json()["bal"]

# Checking balance for p2

balData={
    "pub":publicKeyP2,
}
b2 = requests.get(combine(host,p1,'balance'), json=balData).json()["bal"]

balData={
    "pub":publicKeyP3,
}
b3 = requests.get(combine(host,p1,'balance'), json=balData).json()["bal"]

print(b1,b2,b3)


signed_object = requests.get(combine(host,p1,'getsigs'),json={"pvt":privateKeyP1}).json()
signature_r = signed_object['r']
signature_s = signed_object['s']
transData={
    "sender":publicKeyP1,   # Why public key?, as we are doing internal hashing of the public key, so we can use the public key
    "receiver":resip,
    "amount":b1,
    "signed_hash":None,
    "signature_r":signature_r,
    "signature_s":signature_s,
}

print("-----------",requests.post(combine(host,p1,'addtxn'),json=transData).status_code)



signed_object = requests.get(combine(host,p2,'getsigs'),json={"pvt":privateKeyP2}).json()
signature_r = signed_object['r']
signature_s = signed_object['s']
transData={
    "sender":publicKeyP2,   # Why public key?, as we are doing internal hashing of the public key, so we can use the public key
    "receiver":resip,
    "amount":b2,
    "signed_hash":None,
    "signature_r":signature_r,
    "signature_s":signature_s,
}

print("-----------",requests.post(combine(host,p1,'addtxn'),json=transData).status_code)


signed_object = requests.get(combine(host,p3,'getsigs'),json={"pvt":privateKeyP3}).json()
signature_r = signed_object['r']
signature_s = signed_object['s']
transData={
    "sender":publicKeyP3,   # Why public key?, as we are doing internal hashing of the public key, so we can use the public key
    "receiver":resip,
    "amount":b3,
    "signed_hash":None,
    "signature_r":signature_r,
    "signature_s":signature_s,
}

print("-----------",requests.post(combine(host,p1,'addtxn'),json=transData).status_code)

