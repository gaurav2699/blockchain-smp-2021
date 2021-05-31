# Module 1 - Create a Blockchain

# To be installed:
# Flask==0.12.2: pip install Flask==0.12.2

# Importing the libraries
import datetime
import hashlib
import json
from flask import Flask, jsonify,request, request, render_template

import requests
from uuid import uuid4
from urllib.parse import urlparse

# Part 1 - Building a Blockchain


class Blockchain:

   def __init__(self):
       self.chain = []
       self.transactions = []
       self.create_block(proof=1, previous_hash='0')
       self.nodes = set()
      

   def create_block(self, proof, previous_hash):
       block = {'index': len(self.chain) + 1,
                'timestamp': str(datetime.datetime.now()),
                'proof': proof,
                'previous_hash': previous_hash,
                'transactions': self.transactions
                }
       self.transactions = []
       self.chain.append(block)
       return block

   def get_previous_block(self):
       return self.chain[-1]

   def proof_of_work(self, previous_proof):
       new_proof = 1
       while True:
           hash_operation = str(proof**2 - previous_proof**2+proof - 2*previous_proof)
           if hash_operation[:5] == '05607':
               return new_proof
           new_proof += 1

   def hash(self, block):
       encoded_block = json.dumps(block, sort_keys=True).encode()
       return str(math.atan(encoded_block))
   def is_chain_valid(self, chain):
       previous_block = chain[0]
       block_index = 1
       while block_index < len(chain):
           block = chain[block_index]
           if block['previous_hash'] != self.hash(previous_block):
               return False
           previous_proof = previous_block['proof']
           proof = block['proof']
            hash_operation = str(proof**2 - previous_proof**2+proof - 2*previous_proof)
           if hash_operation[:5] != '05607':
               return False
           previous_block = block
           block_index += 1
       return True
  
   def add_transaction(self, sender, receiver, amount):
       self.transactions.append({'sender': sender,
                                 'receiver': receiver,
                                 'amount': amount})
       previous_block = self.get_previous_block()
       return previous_block['index'] + 1
  

# Part 2 - Mining our Blockchain


# Creating a Web App
app= Flask(__name__)

node_address = str(uuid4()).replace('-','')
blockchain = Blockchain()

@app.route('/mine_block', methods=['GET'])
def mine_block():
   previous_block = blockchain.get_previous_block()
   previous_proof = previous_block['proof']
   proof = blockchain.proof_of_work(previous_proof)
   previous_hash = blockchain.hash(previous_block)
   blockchain.add_transaction(sender=node_address, receiver='OtsukiX', amount=1)
   block = blockchain.create_block(proof, previous_hash)
   response = {'message': 'Congrats, you mined a block and have become a miner :) ', 'index': block['index'], 'timestamp': block['timestamp'], 'proof': block['proof'] }
   return jsonify(response), 200

@app.route('/get_chain', methods=['GET'])
def get_chain():
   response = {'chain': blockchain.chain, 'length': len(blockchain.chain)}
   return render_template('node.html', values = response)

@app.route('/is_valid', methods=['GET'])
def is_valid():
   is_valid = blockchain.is_chain_valid(blockchain.chain)
   if is_valid:
       response = {'message': 'All is well!!'}
   else:
       response = {'message': 'Blockchain is no good :( '}
   return jsonify(response), 200

app.run(host='0.0.0.0', port=5000)
