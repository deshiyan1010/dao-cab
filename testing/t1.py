import requests
import json

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
