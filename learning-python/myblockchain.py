import hashlib
import json
from collections import deque
from time import time
from uuid import uuid4
from flask import Flask, jsonify, request


class MyBlockChain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = deque()
        # Start the genesis block
        self.new_block(previous_hash='1', proof=100)
        self.add_routes()

    def new_block(self, proof: int, previous_hash: str = None) -> dict:
        # Create a new Block and add to current chain
        """
        :param proof:
        :param previous_hash:
        :return:
        """
        block = {
            'index': len(self.chain),
            'timestamp': time(),
            'transactions': list(self.current_transactions),
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Reset the current list of transactions
        self.current_transactions.clear()
        self.chain.append(block)
        return block

    def proof_of_work(self, last_proof: int) -> int:
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
    def valid_proof(last_proof: int, proof: int) -> bool:
        """
        Validates the proof: Does hash(last_proof, proof) contain 4 leading zeros?
        :param last_proof:
        :param proof:
        :return:
        """
        guess = f"{last_proof}{proof}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()

        return guess_hash[:4] == "0000"

    def new_transaction(self, sender: str, recipient: str, amount: int) -> int:
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
    def hash(block: dict
