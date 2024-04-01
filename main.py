from flask import Flask, jsonify, request
import hashlib

blockchain = []

def proof_of_work(last_proof):
    proof = 0
    while valid_proof(last_proof, proof) is False:
        proof += 1
    return proof

def valid_proof(last_proof, proof):
    guess = f'{last_proof}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:4] == "0000"

def calculate_hash(block):
    block_string = str(block['index']) + str(block['transactions']) + str(block['proof']) + block['previous_hash']
    return hashlib.sha256(block_string.encode()).hexdigest()

app = Flask(__name__)

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {'blockchain': blockchain, 'length': len(blockchain)}
    return jsonify(response)

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400
    index = len(blockchain) + 1
    transaction = {
        'sender': values['sender'],
        'recipient': values['recipient'],
        'amount': values['amount']
    }
    blockchain.append(transaction)
    return jsonify({'message': f'Transaction added to Block {index}'})

@app.route('/mine', methods=['GET'])
def mine_block():
    last_block = blockchain[-1]
    last_proof = last_block['proof']
    proof = proof_of_work(last_proof)
    
    blockchain.append({
        'index': len(blockchain) + 1,
        'transactions': [{'sender': '0', 'recipient': 'miner_address', 'amount': 1}],
        'proof': proof,
        'previous_hash': calculate_hash(last_block)
    })
    
    return 'Block mined successfully'

if __name__ == '__main__':
    app.run(port=5000)
