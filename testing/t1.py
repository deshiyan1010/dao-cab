import requests
import json

def combine(ip,port,path):
    return "http://"+ip+":"+port+"/"+path

host = "0.0.0.0"

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
