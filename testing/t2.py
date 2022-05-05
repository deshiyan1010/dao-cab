
import requests
import json
from pprint import pprint



import requests
import json
from pprint import pprint

def combine(ip,port,path):
    return "http://"+ip+":"+port+"/"+path

host = "127.0.0.1"

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


obj = requests.get(combine(host,p3,'getkey')).json()
pub = obj["pub"]
pvt = obj["pvt"]
print(obj)

print(10,requests.get(combine(host,p3,'balance'),json={"pub":pub}).json())

print(11,requests.post(combine(host,p3,'mine')).json())
print(12,requests.post(combine(host,p3,'mine')).json())

print(13,requests.get(combine(host,p3,'balance'),json={"pub":pub}).json())
print(14,end='')
pprint(requests.get(combine(host,p1,'getdata')).json())
print(15,end='')
pprint(requests.get(combine(host,p1,'balance'),json={"pub":pub}).json())