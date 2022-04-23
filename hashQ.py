
from collections import deque
import pickle
import os
import time


class Node:
    def __init__(self,data) -> None:
        self.timestamp = time.time()
        self.data = data




class Queue:
    
    def __init__(self,keep=100):
        self.arr = deque()
        self.keep = keep
        self.locator = {}

    def insert(self,val):
        node = Node(val)
        self.locator[val] = node
        self.arr.append(node)
        
        if len(self.arr)>self.keep:
            popped = self.pop()
            self.locator.pop(popped.data)

    def search(self,data):
        if data in self.locator:
            return True
        return False

    def pop(self):
        return self.arr.popleft() 
    



if __name__=="__main__":
    h = Queue(5)
    h.insert(10)
    h.insert(30)
    h.insert(49)

    o = h.pop()
    print(o.timestamp,o.data)
    o = h.pop()
    print(o.timestamp,o.data)
    