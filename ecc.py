import random

import base64
import hashlib
from Crypto.Cipher import AES
from Crypto import Random
from tinyec import registry
import hashlib, secrets, binascii
from nummaster.basic import sqrtmod

class EllipticCurveCryptography:
    
    def __init__(self):
        self.Pcurve = 2**256 - 2**32 - 2**9 - 2**8 - 2**7 - 2**6 - 2**4 -1 
        self.N=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
        self.Acurve = 0
        self.Bcurve = 7 
        self.Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240
        self.Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424
        self.GPoint = (self.Gx,self.Gy)


    def modinv(self,a,n):
        lm, hm = 1,0
        low, high = a%n,n

        while low > 1:
            ratio = int(high/low)
            nm, new = hm-lm*ratio, high-low*ratio
            lm, low, hm, high = nm, new, lm, low

        return lm % n

    def ECadd(self,a,b):
        LamAdd = ((b[1]-a[1]) * self.modinv(b[0]-a[0],self.Pcurve)) % self.Pcurve
        
        x = (LamAdd*LamAdd-a[0]-b[0]) % self.Pcurve
        y = (LamAdd*(a[0]-x)-a[1]) % self.Pcurve
        return (x,y)

    def ECdouble(self,a):

        Lam = ((3*a[0]*a[0]+self.Acurve) * self.modinv((2*a[1]),self.Pcurve)) % self.Pcurve
        x = (Lam*Lam-2*a[0]) % self.Pcurve
        y = (Lam*(a[0]-x)-a[1]) % self.Pcurve

        return (x,y)

    def EccMultiply(self,GenPoint,ScalarHex): 
        if ScalarHex == 0 or ScalarHex >= self.N: 
            raise Exception("Invalid Scalar/Private Key")
        ScalarBin = str(bin(ScalarHex))[2:]

        Q=GenPoint
        for i in range (1, len(ScalarBin)): 
            Q=self.ECdouble(Q); 
            if ScalarBin[i] == "1":
                Q=self.ECadd(Q,GenPoint)
        return (Q)

    def generate_pvt_key(self):
        a = random.SystemRandom().getrandbits(256)        
        return a

    def generate_ecc_pair(self):
        private_key = self.generate_pvt_key()
        PublicKey = self.EccMultiply(self.GPoint,private_key)
        return PublicKey[0],PublicKey[1],private_key

    def compress_pubKey(self,pubx,puby):
        if puby%2==1:
            return int("1"+hex(pubx)[2:],16)
        return int("2"+hex(pubx)[2:],16)

    def decompress_pubKey(self,pubx):
        hexString = hex(pubx)
        inter = sqrtmod(pow(int(hexString[3:],16), 3, self.Pcurve) + self.Acurve * pubx + self.Bcurve, self.Pcurve)
        if (hexString[2]=="1" and bool(inter & 1)==1) or (hexString[2]=="2" and bool(inter & 1)!=1):
            return (int(hexString[3:],16),inter) 
        else:
            return (int(hexString[3:],16),self.Pcurve-inter)

    def sign(self,private_key,hash=None):
        if hash!=None:
            if isinstance(hash,str):
                hash = int(hash,16)
        else:
            hash = int(hashlib.sha256("random".encode('utf-8')).hexdigest(),16)

        RandNum = self.generate_pvt_key()
        xRandSignPoint, yRandSignPoint = self.EccMultiply(self.GPoint,RandNum)
        r = xRandSignPoint % self.N
        s = ((hash + r*private_key)*(self.modinv(RandNum,self.N))) % self.N
        signed_object = {'r':r,'s':s}
        return signed_object

    def verify(self,pubKey,hash,r,s):
        pubKey = self.decompress_pubKey(pubKey)
        if hash!=None:
            if isinstance(hash,str):
                hash = int(hash,16)
        else:
            hash = int(hashlib.sha256("random".encode('utf-8')).hexdigest(),16)
        w = self.modinv(s,self.N)
        xu1, yu1 = self.EccMultiply(self.GPoint,(hash * w)%self.N)
        xu2, yu2 = self.EccMultiply(pubKey,(r*w)%self.N)
        x,y = self.ECadd((xu1,yu1),(xu2,yu2))
        if r==x:
            return True
        return False

    def create_shared_key(self,others_pub,own_pvt_key):
        return self.EccMultiply(others_pub,own_pvt_key)


    def encrypt_AES_GCM(self,msg, secretKey):
        aesCipher = AES.new(secretKey, AES.MODE_GCM)
        ciphertext, authTag = aesCipher.encrypt_and_digest(msg.encode("utf-8"))
        return (ciphertext, aesCipher.nonce, authTag)

    def decrypt_AES_GCM(self,ciphertext, nonce, authTag, secretKey):
        aesCipher = AES.new(secretKey, AES.MODE_GCM, nonce)
        plaintext = aesCipher.decrypt_and_verify(ciphertext, authTag)
        return plaintext

    def ecc_point_to_256_bit_key(self,point):
        sha = hashlib.sha256(int.to_bytes(point[0], 32, 'big'))
        sha.update(int.to_bytes(point[1], 32, 'big'))
        return sha.digest()

    def encrypt_ECC(self,msg, pubKey):
        ciphertextPrivKey = self.generate_pvt_key()
        sharedECCKey =  self.EccMultiply(self.decompress_pubKey(pubKey),ciphertextPrivKey)
        secretKey = self.ecc_point_to_256_bit_key(sharedECCKey)
        ciphertext, nonce, authTag = self.encrypt_AES_GCM(msg, secretKey)
        ciphertextPubKey = self.EccMultiply(self.GPoint,ciphertextPrivKey)
        enc_obj = {
            'ciphertext':ciphertext,
            'nonce':nonce,
            'authTag':authTag,
            'ciphertextPubKey':ciphertextPubKey
        }
        return enc_obj

    def decrypt_ECC(self,encryptedMsg, privKey):
        ciphertext = encryptedMsg['ciphertext']
        nonce = encryptedMsg['nonce']
        authTag = encryptedMsg['authTag']
        ciphertextPubKey = encryptedMsg['ciphertextPubKey']
        sharedECCKey = self.EccMultiply(ciphertextPubKey,privKey)
        secretKey = self.ecc_point_to_256_bit_key(sharedECCKey)
        plaintext = self.decrypt_AES_GCM(ciphertext, nonce, authTag, secretKey)
        return plaintext


if __name__=="__main__":
    e = EllipticCurveCryptography()
    p1,p2,pvt = e.generate_ecc_pair()
    comp = e.compress_pubKey(p1,p2)
    message = "hello"
    hashed = hashlib.sha256(message.encode('utf-8')).hexdigest()
    print("1",int(hashed,16))
    t = e.encrypt_ECC(message,comp)
    print("2",t)
    signed = e.sign(pvt)
    print("3",signed)
    verify = e.verify(comp,None,signed['r'],signed['s'])
    print("4",verify)
    print("5",e.decrypt_ECC(t,pvt))