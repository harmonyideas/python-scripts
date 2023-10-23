import hashlib
import json
from time import time
from uuid import uuid4
from flask import Flask, jsonify, request

class Blockchain:
   def __init__(self):
       self.chain = []
       self.current_transactions = []
       # Start the genesis block
       self.new_block(previous_hash='1', proof=100)

   def new_block(self, proof, previous_hash=None):
       block = {
           'index': len(self.chain),
           'timestamp': time(),
           'transactions': self.current_transactions,
           'proof': proof,
           'previous_hash': previous_hash or self.hash(self.chain[-1]),
       }

       self.current_transactions = []
       self.chain.append(block)
       return block

   def proof_of_work(self, last_proof):
       proof = 0
       while self.valid_proof(last_proof, proof) is False:
           proof += 1

       return proof

   @staticmethod
   def valid_proof(last_proof, proof):
       guess = '{last_proof}{proof}'.encode()
       guess_hash = hashlib.sha256(guess).hexdigest()

       return guess_hash[:4] == "0000"

   def new_transaction(self, sender, recipient, amount):
       self.current_transactions.append({
           'sender': sender,
           'recipient': recipient,
           'amount': amount,
       })

   @staticmethod
   def hash(block):
       block_string = json.dumps(block, sort_keys=True).encode()
       return hashlib.sha256(block_string).hexdigest()

   @property
   def last_block(self):
       return self.chain[-1]


# Instantiate a new Blockchain
blockchain = Blockchain()

# Create a Flask app
app = Flask(__name__)


# Create a new route to mine a block
@app.route('/mine', methods=['GET'])
def mine():
    # Get the last block in the chain
    last_block = blockchain.last_block

    # Get the last proof
    last_proof = last_block['proof']

    # Calculate the new proof
    proof = blockchain.proof_of_work(last_proof)

    # Create a new transaction to reward the miner
    blockchain.new_transaction(sender="0", recipient=app.config['NODE_IDENTIFIER'], amount=1)

    # Create a new block
    block = blockchain.new_block(proof, previous_hash=last_block['hash'])

    # Respond with the new block
    return jsonify({
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }), 200


# Create a new route to add a new transaction
@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    # Get the transaction data from the request body
    values = request.get_json()

    # Check that all the required fields are present
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    # Respond with the transaction index
    return jsonify({
        'message': 'Transaction will be added to Block {index}
