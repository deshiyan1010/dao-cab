from collections import defaultdict
from turtle import pu
from math import log10

class GIS:

    def __init__(self,precision):
        self.precision = precision
        self.bucket = defaultdict(list)
        self.linker = {}

    def addToBucket(self,lat,long,pubKey,data):
        centric_lat,centric_long = self.convert(lat,long)
        self.bucket[(centric_lat,centric_long)].append((lat,long,pubKey))
        self.linker[pubKey] = (lat,long,data)

    def remove(self,pubKey):
        lat,long,data = self.linker[pubKey]
        c_lat,c_long = self.convert(lat,long)
        self.bucket[(c_lat,c_long)].remove((lat,long,pubKey))
        self.linker.pop(pubKey)
        return lat,long,data
    
    def query(self,lat,long):
        c_lat,c_long = self.convert(lat,long)
        return self.bucket[(c_lat,c_long)]

    def convert(self,lat,long):
        c_lat = (lat//self.precision)*self.precision
        c_long = (long//self.precision)*self.precision
        
        rounding = int(-log10(self.precision)+2)

        c_lat = round(c_lat,rounding)
        c_long = round(c_long,rounding)
        return c_lat,c_long

    def get_radius(self,k,lat,long):
        k = int(k)
        query_response = []
        # k-=1
        print(k,"\n"*5)
        c_lat,c_long = self.convert(lat,long)
        c_lat-=self.precision*k 
        c_long-=self.precision*k 

        for i in range(2*k):
            q_c_long = c_long+self.precision*i
            if q_c_long>=360:
                q_c_long = q_c_long-360
            for j in range(2*k):
                q_c_lat = c_lat+self.precision*j 
                print(q_c_lat,q_c_long)
                query_response.extend(self.bucket[(q_c_lat,q_c_long)])
        
        return query_response


if __name__=="__main__":
    obj = GIS(1)
    obj.addToBucket(12.92478,77.49999,20)
    print(obj.query(12,77))
    print(obj.addToBucket(32,0.9,77))
    print(obj.get_radius(5,30,359))


