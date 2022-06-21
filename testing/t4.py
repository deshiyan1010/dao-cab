from time import sleep
import requests
import json
from pprint import pprint
import sys 
sys.path.append('..')
from ecc import EllipticCurveCryptography
from pprint import pprint



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



# transData={
#     "passenger":publicKeyP1,   # Why public key?, as we are doing internal hashing of the public key, so we can use the public key
#     "pick_loc":(0.1,0.1),
#     "drop_loc":(0.2,0.1),
#     "signed_hash":None,
#     "signature_r":signature_r,
#     "signature_s":signature_s,
# }

# print("-----------",requests.post(combine(host,p1,'bookride'),json=transData).json())




# #AFTER RIDE REQUEST SUBMISSION
# #IN P1
# jsonx = {"pubKey":"0x2b2498eca454c17a7762f59b84c43dea78e015b5745437ddf973a86860125ba1f"}
# print(5, "Rider")
# print(requests.get(combine(host,p1,'explore'), json=jsonx).json()['activeRequest'])

# #IN P2
# jsonx = {"pubKey":"0x2b2498eca454c17a7762f59b84c43dea78e015b5745437ddf973a86860125ba1f"}
# print(7, "Rider")
# print(requests.get(combine(host,p2,'explore'), json=jsonx).json()['activeRequest'])

# #IN P3
# jsonx = {"pubKey":"0x2b2498eca454c17a7762f59b84c43dea78e015b5745437ddf973a86860125ba1f"}
# print(9, "Rider")
# print(requests.get(combine(host,p3,'explore'), json=jsonx).json()['activeRequest'])



# #Getting list

# jsonx = {'k':1,'lat':0.10001,'long':0.1005}
# print(10,requests.get(combine(host,p3,'listride'), json=jsonx).json())



# #Bidding
# jsonx = {'passenger':publicKeyP1,'provider':publicKeyP2,'bid':1}
# print(11,requests.post(combine(host,p3,'bidride'), json=jsonx).json())

# print("Bid placed")
# print(12,requests.get(combine(host,p1,'bidlist'), json=jsonx).json())
# print(13,requests.get(combine(host,p2,'bidlist'), json=jsonx).json())
# print(14,requests.get(combine(host,p3,'bidlist'), json=jsonx).json())



# jsonx = {'passenger':publicKeyP1,'provider':publicKeyP3,'bid':1}
# print(15,requests.post(combine(host,p3,'bidride'), json=jsonx).json())

# print("Bid placed")
# print(16,requests.get(combine(host,p1,'bidlist'), json=jsonx).json())
# print(17,requests.get(combine(host,p2,'bidlist'), json=jsonx).json())
# print(18,requests.get(combine(host,p3,'bidlist'), json=jsonx).json())



# #Selecting bid
# transData={
#     "passenger":publicKeyP1,  
#     "provider":publicKeyP2,
#     "signed_hash":None,
#     "signature_r":signature_r,
#     "signature_s":signature_s,
# }
# print(19,requests.post(combine(host,p3,'selbidride'), json=transData).json())

# jsonx = {"pubKey":"0x2b2498eca454c17a7762f59b84c43dea78e015b5745437ddf973a86860125ba1f"}
# print(20, "Rider")
# print(requests.get(combine(host,p1,'explore'), json=jsonx).json()['activeRequest'])

# #IN P2
# jsonx = {"pubKey":"0x2b2498eca454c17a7762f59b84c43dea78e015b5745437ddf973a86860125ba1f"}
# print(21, "Rider")
# print(requests.get(combine(host,p2,'explore'), json=jsonx).json()['activeRequest'])

# #IN P3
# jsonx = {"pubKey":"0x2b2498eca454c17a7762f59b84c43dea78e015b5745437ddf973a86860125ba1f"}
# print(22, "Rider")
# print(requests.get(combine(host,p3,'explore'), json=jsonx).json()['activeRequest'])

# jsonx = {'k':1,'lat':0.10001,'long':0.1005}
# print(23,requests.get(combine(host,p3,'listride'), json=jsonx).json())

#End ride

#IN P1
# jsonx = {"pubKey":"0x2b2498eca454c17a7762f59b84c43dea78e015b5745437ddf973a86860125ba1f"}
# print(5, "Rider")
# print(requests.get(combine(host,p1,'explore'), json=jsonx).json()['activeRequest'])

# #IN P2
# jsonx = {"pubKey":"0x2b2498eca454c17a7762f59b84c43dea78e015b5745437ddf973a86860125ba1f"}
# print(7, "Rider")
# print(requests.get(combine(host,p2,'explore'), json=jsonx).json()['activeRequest'])

# #IN P3
# jsonx = {"pubKey":"0x2b2498eca454c17a7762f59b84c43dea78e015b5745437ddf973a86860125ba1f"}
# print(9, "Rider")
# print(requests.get(combine(host,p3,'explore'), json=jsonx).json()['activeRequest'])

# transData={
#     "passenger":publicKeyP1,  
#     "provider":publicKeyP2,
#     "signed_hash":None,
#     "signature_r":signature_r,
#     "signature_s":signature_s,
# }
# print(requests.post(combine(host,p3,'endride'), json=transData).json())

# #IN P1
# jsonx = {"pubKey":"0x2b2498eca454c17a7762f59b84c43dea78e015b5745437ddf973a86860125ba1f"}
# print(5, "Rider")
# print(requests.get(combine(host,p1,'explore'), json=jsonx).json()['activeRequest'])

# #IN P2
# jsonx = {"pubKey":"0x2b2498eca454c17a7762f59b84c43dea78e015b5745437ddf973a86860125ba1f"}
# print(7, "Rider")
# print(requests.get(combine(host,p2,'explore'), json=jsonx).json()['activeRequest'])

# #IN P3
# jsonx = {"pubKey":"0x2b2498eca454c17a7762f59b84c43dea78e015b5745437ddf973a86860125ba1f"}
# print(9, "Rider")
# print(requests.get(combine(host,p3,'explore'), json=jsonx).json()['activeRequest'])


# #AFTER RIDE END
# #IN P1
# jsonx = {"pubKey":"0x2b2498eca454c17a7762f59b84c43dea78e015b5745437ddf973a86860125ba1f"}
# print(24, "Rider")
# pprint(requests.get(combine(host,p1,'explore'), json=jsonx).json()['ridetaken'])

# jsonx = {"pubKey":"0x186aee1d9870df32c59030e7dc9a0aec72b28e9d3f9fa19f91f799ddee4c59662"}
# print(25, "Provider")
# pprint(requests.get(combine(host,p1,'explore'), json=jsonx).json()['rideprovided'])


# #IN P2
# jsonx = {"pubKey":"0x2b2498eca454c17a7762f59b84c43dea78e015b5745437ddf973a86860125ba1f"}
# print(26, "Rider")
# pprint(requests.get(combine(host,p2,'explore'), json=jsonx).json()['ridetaken'])

# jsonx = {"pubKey":"0x186aee1d9870df32c59030e7dc9a0aec72b28e9d3f9fa19f91f799ddee4c59662"}
# print(27, "Provider")
# pprint(requests.get(combine(host,p2,'explore'), json=jsonx).json()['rideprovided'])


# #IN P3
# jsonx = {"pubKey":"0x2b2498eca454c17a7762f59b84c43dea78e015b5745437ddf973a86860125ba1f"}
# print(28, "Rider")
# pprint(requests.get(combine(host,p3,'explore'), json=jsonx).json()['ridetaken'])

# jsonx = {"pubKey":"0x186aee1d9870df32c59030e7dc9a0aec72b28e9d3f9fa19f91f799ddee4c59662"}
# print(29, "Provider")
# pprint(requests.get(combine(host,p3,'explore'), json=jsonx).json()['rideprovided'])


jsonx = {"pubKey":"0x2b2498eca454c17a7762f59b84c43dea78e015b5745437ddf973a86860125ba1f"}
print(20, "Rider")
pprint(requests.get(combine(host,p1,'explore'), json=jsonx).json())

jsonx = {"pubKey":"0x186aee1d9870df32c59030e7dc9a0aec72b28e9d3f9fa19f91f799ddee4c59662"}
print(20, "Provider")
pprint(requests.get(combine(host,p1,'explore'), json=jsonx).json())