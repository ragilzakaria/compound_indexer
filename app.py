from web3 import Web3

"""
Database SQLite - file based (vs. server based)
Web/API: Flask
Object-relation mapping: Alchemy
Web3 RPC: Infura
ABI: etherscan


Request-response flow:
HTTP call -> Webserver -> Flask -> Database

Ingestion flow:
Smart contract (compound) -> events (Borrow, Mint) -> rpc/infura -> follow -> database
"""

from flask import Flask, jsonify
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
infura_url = os.getenv('INFURA_URL')
web3 = Web3(Web3.HTTPProvider(infura_url))


@app.route("/user/<address>/points", methods=["GET"])
def get_compound_points(address):
    # Validate the address format
    if not web3.is_address(address):
        return jsonify({'error': 'Invalid address format'}), 400

    points = 0

    return jsonify({
        'address': address,
        'points': points
    })


if __name__ == "__main__":
    app.run(debug=True) # need to set false in production
