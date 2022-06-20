from time import sleep
import requests
import json
from pprint import pprint
import sys 
sys.path.append('..')
from ecc import EllipticCurveCryptography



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
ecc = EllipticCurveCryptography()
print(privateKeyP1)
signed_object = ecc.sign(privateKeyP1)
signature_r = signed_object['r']
signature_s = signed_object['s']


balData={
    "pub":publicKeyP1,
}
print(6,requests.get(combine(host,p1,'balance'), json=balData).json())

# Checking balance for p2

balData={
    "pub":publicKeyP2,
}
print(7,requests.get(combine(host,p2,'balance'), json=balData).json())

balData={
    "pub":publicKeyP3,
}
print(8,requests.get(combine(host,p3,'balance'), json=balData).json())

print("before transaction")

transData={
    "sender":publicKeyP1,   # Why public key?, as we are doing internal hashing of the public key, so we can use the public key
    "receiver":publicKeyP3,
    "amount":1,
    "signed_hash":None,
    "signature_r":signature_r,
    "signature_s":signature_s,
}

print("-----------",requests.post(combine(host,p1,'addtxn'),json=transData).json())



print("Transaction added from p1 to p2")


# Testing the getdata mempool function

print(9,requests.get(combine(host,p1,'getdata')).json()['mempool_txn'])
print(10,requests.get(combine(host,p2,'getdata')).json()['mempool_txn'])
print(11,requests.get(combine(host,p3,'getdata')).json()['mempool_txn'])


# Mining to verify the transaction in mempool

# print(requests.post(combine(host,p1,'mine'),json={}).json())
# print(requests.post(combine(host,p2,'mine'),json={}).json())
print(12,requests.post(combine(host,p3,'mine'),json={}).json())


print(13,requests.get(combine(host,p1,'getdata')).json()['mempool_txn'])
print(14,requests.get(combine(host,p2,'getdata')).json()['mempool_txn'])
print(15,requests.get(combine(host,p3,'getdata')).json()['mempool_txn'])


# print(requests.post(combine(host,p2,'mine'),json={}).json())

# print(requests.post(combine(host,p1,'mine'),json={}).json())
# print(requests.post(combine(host,p1,'mine'),json={}).json())

# print(requests.post(combine(host,p2,'mine'),json={}).json())

# Checking balance for p1
balData={
    "pub":publicKeyP1,
}
print(16,requests.get(combine(host,p1,'balance'), json=balData).json())
print(17,requests.get(combine(host,p2,'balance'), json=balData).json())
print(18,requests.get(combine(host,p3,'balance'), json=balData).json())

# Checking balance for p2

balData={
    "pub":publicKeyP2,
}
print(19,requests.get(combine(host,p1,'balance'), json=balData).json())
print(20,requests.get(combine(host,p2,'balance'), json=balData).json())
print(21,requests.get(combine(host,p3,'balance'), json=balData).json())

balData={
    "pub":publicKeyP3,
}
print(22,requests.get(combine(host,p1,'balance'), json=balData).json())
print(23,requests.get(combine(host,p2,'balance'), json=balData).json())
print(24,requests.get(combine(host,p3,'balance'), json=balData).json())

# balData={
#     "pub":publicKeyP3,
# }
# print(requests.get(combine(host,p3,'balance'), json=balData).json())
# print("hello")


print(publicKeyP3)
jsonx = {"pubKey":312225830859370951780608748925173258727083128049137890652641525295514472790559}

from pprint import pprint

print(25)
pprint(requests.get(combine(host,p1,'explore'), json=jsonx).json())
