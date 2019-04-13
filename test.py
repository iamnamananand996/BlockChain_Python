import datetime
import hashlib
import json
from flask import Flask, jsonify,render_template,url_for
from flask_bootstrap import Bootstrap


class Blockchain:

    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.create_block(proof= 1, previous_hash ='0')

    def create_block(self,proof,previous_hash):
        block= {'index': len(self.chain) + 1 ,
                'timestamp': str(datetime.datetime.now()),
                'transactions': self.current_transactions,
                'proof': proof,
                'previous_hash': previous_hash}
        
        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        sender = self.hash(sender)
        recipient = self.hash(recipient)
        amount = self.hash(amount)
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })

        # return self.get_previous_block['index'] + 1


    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof=1
        check_proof= False
        while check_proof is False:
           #condition applied by you
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof =True
            else:
                new_proof  +=1
        return new_proof

    def hash(self,block):
        encoded_block = json.dumps(block,sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self,chain):
        previous_block= chain[0]
        block_index= 1
        while block_index <len(chain):
            block =chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False

            previous_proof =previous_block['proof']
            proof =block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] !='0000':
                return False
            previous_block=block
            block_index +=1
        return True


# Block = Blockchain()
# x = Block.create_block('0','F')
# y = Block.is_chain_valid(x)
# print(y)

app = Flask(__name__)
Bootstrap(app)

blockchain = Blockchain()


@app.route('/')
def main():
    return render_template('index.html')

@app.route('/mine_block', methods = ['GET'])
def mine_block():

    blockchain.new_transaction(
        sender="0",
        recipient='data',
        amount=1,
    )

    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message': 'Block Is Mined',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'transactions' : block['transactions'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']}
    return jsonify(response), 200


@app.route('/print_chain',methods=['GET'])
def print_chain():
    response ={'chain':blockchain.chain,
    'lenght ':len(blockchain.chain)}

    return jsonify(response), 200

@app.route('/check_blockchain',methods = ['GET'])
def check_blockchain():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': 'The Blockchain is Right.'}
    else:
        response = {'message': 'The Blockchain is not Right.'}
    return jsonify(response), 200


# app.run(host = '0.0.0.0', port = 5000)
if __name__ == "__main__":
    app.run(debug=True)