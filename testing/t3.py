from time import sleep
import requests
import json
from pprint import pprint
from ecc import EllipticCurveCryptography



def combine(ip,port,path):
    return "http://"+ip+":"+port+"/"+path

host = "127.0.0.1"
# "http://"+"127.0.0.1"+":"+"5000"+"/"+getdata
p1 = "5000"
p2 = "5001"
p3 = "5003"


# Connecting the nodes p2 and p3 to p1 and checking p1's neighbors

data = {
    "ip":host,
    "port":p2
    }
print(requests.post(combine(host,p1,'connect'),json=data).json())
print(requests.get(combine(host,p1,'neighbors')).json())


data = {
    "ip":host,
    "port":p3
    }
print(requests.post(combine(host,p2,'connect'),json=data).json())
print(requests.get(combine(host,p2,'neighbors')).json())

# mining on p1

print(requests.post(combine(host,p1,'mine'),json={}).json())

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
signed_object = ecc.sign(privateKeyP1)
signature_r = signed_object['r']
signature_s = signed_object['s']


balData={
    "pub":publicKeyP1,
}
print(requests.get(combine(host,p1,'balance'), json=balData).json())

# Checking balance for p2

balData={
    "pub":publicKeyP2,
}
print(requests.get(combine(host,p2,'balance'), json=balData).json())

balData={
    "pub":publicKeyP3,
}
print(requests.get(combine(host,p3,'balance'), json=balData).json())

print("before transaction")

transData={
    "sender":publicKeyP1,   # Why public key?, as we are doing internal hashing of the public key, so we can use the public key
    "receiver":publicKeyP3,
    "amount":1,
    "signed_hash":None,
    "signature_r":signature_r,
    "signature_s":signature_s,
}

requests.post(combine(host,p1,'addtxn'),json=transData)



print("Transaction added from p1 to p2")


# Testing the getdata mempool function

print(requests.get(combine(host,p1,'getdata')).json()['mempool_txn'])
print(requests.get(combine(host,p2,'getdata')).json()['mempool_txn'])
print(requests.get(combine(host,p3,'getdata')).json()['mempool_txn'])


# Mining to verify the transaction in mempool

# print(requests.post(combine(host,p1,'mine'),json={}).json())
# print(requests.post(combine(host,p2,'mine'),json={}).json())
print(requests.post(combine(host,p3,'mine'),json={}).json())


print(requests.get(combine(host,p1,'getdata')).json()['mempool_txn'])
print(requests.get(combine(host,p2,'getdata')).json()['mempool_txn'])
print(requests.get(combine(host,p3,'getdata')).json()['mempool_txn'])


# print(requests.post(combine(host,p2,'mine'),json={}).json())

# print(requests.post(combine(host,p1,'mine'),json={}).json())
# print(requests.post(combine(host,p1,'mine'),json={}).json())

# print(requests.post(combine(host,p2,'mine'),json={}).json())

# Checking balance for p1
balData={
    "pub":publicKeyP1,
}
print(requests.get(combine(host,p1,'balance'), json=balData).json())

# Checking balance for p2

balData={
    "pub":publicKeyP2,
}
print(requests.get(combine(host,p2,'balance'), json=balData).json())

balData={
    "pub":publicKeyP3,
}
print(requests.get(combine(host,p3,'balance'), json=balData).json())

# balData={
#     "pub":publicKeyP3,
# }
# print(requests.get(combine(host,p3,'balance'), json=balData).json())
# print("hello")