from base64 import b32encode
from time import sleep
import requests
import json
from pprint import pprint
import sys 
sys.path.append('..')
from ecc import EllipticCurveCryptography
import time

pro = "0x196e508e51bd9e8a1aac012bc71529b04b8147882ac340891e69210f8f06ae4cb"
cust = "0x254dd50c8c59434bb0cd3d7dd4cb513c2c768221472080ee57fe118858d5a6767"
pro2 = "0x17c2b3d7119654288da94c6cac86be96ee19f031336fbaa757064c0b357fa020a"

def combine(ip,port,path):
    return "http://"+ip+":"+port+"/"+path

host = "0.0.0.0"
# "http://"+"127.0.0.1"+":"+"5000"+"/"+getdata
p1 = "5001"
p2 = "5002"
p3 = "5003"


###########
data = {
    "ip":host,
    "port":p2
    }
print(1,requests.post(combine(host,p1,'connect'),json=data).json())
print(2,requests.get(combine(host,p1,'neighbors')).json())

###########
data = {
    "ip":host,
    "port":p3
    }
print(3,requests.post(combine(host,p1,'connect'),json=data).json())
print(4,requests.get(combine(host,p1,'neighbors')).json())


############
print(5,requests.get(combine(host,p1,'neighbors')).json())
print(6,requests.get(combine(host,p2,'neighbors')).json())
print(7,requests.get(combine(host,p3,'neighbors')).json())

print(8,requests.get(combine(host,p3,'rnfn')).json())
print(9,requests.get(combine(host,p3,'neighbors')).json())



jsonx = {'passenger':cust,"time":time.time()}


jsonx = {'passenger':cust,'provider':pro,'bid':3.12,"time":time.time()}
print(15,requests.post(combine(host,p3,'bidride'), json=jsonx).json())

# jsonx = {'passenger':cust,'provider':pro2,'bid':3.14112,"time":time.time()}
# print(15,requests.post(combine(host,p1,'bidride'), json=jsonx).json())

print(requests.get(combine(host,p1,'bidlist'), json=jsonx).json())
