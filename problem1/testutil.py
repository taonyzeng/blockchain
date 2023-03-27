from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import pkcs1_15
from Cryptodome.Hash import SHA256

def generateKeyPair():
    keyPair = RSA.generate(2048)
    return keyPair

def createSignature(message, privateKey):
    messageHash = SHA256.new(message)
    signer = pkcs1_15.new(privateKey)
    signature = signer.sign(messageHash)
    return signature

def getSha256Hash(message):
    messageBytes = message.encode('utf-8')
    messageHash = SHA256.new(messageBytes)
    return messageHash.digest()



