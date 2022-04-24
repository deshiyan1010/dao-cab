
import requests
import json
from pprint import pprint

def combine(ip,port,path):
    return "http://"+ip+":"+port+"/"+path

host = "127.0.0.1"

p1 = "5000"
p2 = "5001"
p3 = "8008"


# obj = requests.get(combine(host,p1,'getkey')).json()
# pub = obj["pub"]
# pvt = obj["pvt"]
# print(obj)

# print(requests.get(combine(host,p1,'balance'),json={"pub":pub}).json())

# print(requests.post(combine(host,p1,'mine')).json())
# print(requests.post(combine(host,p1,'mine')).json())

# print(requests.get(combine(host,p1,'balance'),json={"pub":pub}).json())
# pprint(requests.get(combine(host,p1,'getdata')).json())

###########
data = {
    "ip":host,
    "port":p2
    }
print(requests.post(combine(host,p1,'connect'),json=data).json())
print(requests.get(combine(host,p1,'neighbors')).json())

###########
data = {
    "ip":host,
    "port":p3
    }
print(requests.post(combine(host,p1,'connect'),json=data).json())
print(requests.get(combine(host,p1,'neighbors')).json())


############
print(requests.get(combine(host,p1,'neighbors')).json())
print(requests.get(combine(host,p2,'neighbors')).json())
print(requests.get(combine(host,p3,'neighbors')).json())

print(requests.get(combine(host,p3,'rnfn')).json())
print(requests.get(combine(host,p3,'neighbors')).json())





import requests
import json
from pprint import pprint

def combine(ip,port,path):
    return "http://"+ip+":"+port+"/"+path

host = "127.0.0.1"

p1 = "5000"
p2 = "5001"
p3 = "8008"




###########
data = {
    "ip":host,
    "port":p2
    }
print(requests.post(combine(host,p1,'connect'),json=data).json())
print(requests.get(combine(host,p1,'neighbors')).json())

###########
data = {
    "ip":host,
    "port":p3
    }
print(requests.post(combine(host,p1,'connect'),json=data).json())
print(requests.get(combine(host,p1,'neighbors')).json())


############
print(requests.get(combine(host,p1,'neighbors')).json())
print(requests.get(combine(host,p2,'neighbors')).json())
print(requests.get(combine(host,p3,'neighbors')).json())

print(requests.get(combine(host,p3,'rnfn')).json())
print(requests.get(combine(host,p3,'neighbors')).json())


obj = requests.get(combine(host,p3,'getkey')).json()
pub = obj["pub"]
pvt = obj["pvt"]
print(obj)

print(requests.get(combine(host,p3,'balance'),json={"pub":pub}).json())

print(requests.post(combine(host,p3,'mine')).json())
print(requests.post(combine(host,p3,'mine')).json())

print(requests.get(combine(host,p3,'balance'),json={"pub":pub}).json())
pprint(requests.get(combine(host,p1,'getdata')).json())
pprint(requests.get(combine(host,p1,'balance'),json={"pub":pub}).json())