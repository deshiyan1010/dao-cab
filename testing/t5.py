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

c1 = requests.get(combine(host,p1,'meta')).json()
c2 = requests.get(combine(host,p2,'meta')).json()
c3 = requests.get(combine(host,p3,'meta')).json()

print(json.dumps(c1)==json.dumps(c2),json.dumps(c2)==json.dumps(c3))
pprint(c1)
pprint(c2)
pprint(c3)