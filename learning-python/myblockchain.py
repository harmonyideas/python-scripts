import hashlib
import json
from time import time
from uuid import uuid4
from flask import Flask, jsonify, request


class MyBlockChain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        # Start the genesis block
        self.new_block(previous_hash='1', proof=100)
        self.add_routes()

    def new_block(self, proof, previous_hash=None):
        # Create a new Block and add to current chain
        """
        :param proof:
        :param previous_hash:
        :return:
        """
        block = {
            'index': len(self.chain),
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Reset the current list of transactions
        self.current_transactions = []
        self.chain.append(block)
        return block

    def proof_of_work(self, last_proof):
        """
        - Find a number p' such that hash(pp') contains 4 leading zeros
        - p is the previous proof, p' is new
        :param last_proof:
        :return:
        """
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Validates the proof: Does hash(last_proof, proof) contain 4 leading zeros?

        :param last_proof:
        :param proof:
        :return:
        """
        guess = '{last_proof}{proof}'.encode().format(last_proof=last_proof,proof=proof)
        guess_hash = hashlib.sha256(guess).hexdigest()

        return guess_hash[:4] == "0000"

    def new_transaction(self, sender, recipient, amount):
        # Adds a new transaction to the list of transactions

        """
        :param sender: <str> Address of the Sender
        :param recipient: <str> Address of the Recipient
        :param amount: <int> Amount
        :return: <int> The index of the Block that will hold this transaction

        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        """
        # Hashes a block SHA-256

        :param block:
        :return:

        """

        # Dictionary must be ordered
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        # Returns the last Block in the chain
        return self.chain[-1]

    def add_routes(self):
        @app.route('/mine', methods=['GET'])
        def mine():
            # Run the proof of work algorithm to get the next proof...
            last_block = blockchain.last_block
            last_proof = last_block['proof']
            proof = blockchain.proof_of_work(last_proof)

            blockchain.new_transaction(
                sender="0",
                recipient=node_identifier,
                amount=1,
            )

            # Form the new Block by adding it to the chain
            previous_hash = blockchain.hash(last_block)
            block = blockchain.new_block(proof, previous_hash)

            response = {
                'message': "New Block Forged",
                'index': block['index'],
                'transactions': block['transactions'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash'],

            }
            return jsonify(response), 200

        @app.route('/transactions/new', methods=['POST'])
        def new_transaction():
            values = request.get_json()

            # Check that the fields are in the POST data
            required = ['sender', 'recipient', 'amount']
            if not all(k in values for k in required):
                return 'Missing values', 400

            # Create a new transaction
            index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])
            response = {'message': 'Transaction will be added to Block {index}'}

            return jsonify(response), 201

        @app.route('/chain', methods=['GET'])
        def full_chain(self):
            response = {'chain': self.blockchain.chain, 'length': len(self.blockchain.chain)}
            return jsonify(response), 200


# Instantiate our Node
app = Flask(__name__)

# Generate a unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = MyBlockChain()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
