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
from flask_restx import Api, Resource, fields
from web3 import Web3
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Set up Web3 connection (connect to Ethereum via Infura)
infura_url = os.getenv('INFURA_URL')
web3 = Web3(Web3.HTTPProvider(infura_url))

# Initialize Flask-RESTX API
api = Api(app, version='1.0', title='Compound v2 API', description='API to fetch user points from Compound v2')

# Define the response model for the API using Flask-RESTX fields
points_model = api.model('Points', {
    'address': fields.String(description='The Ethereum address of the user', required=True),
    'points': fields.Integer(description='The amount of points for the user')
})

# Define the namespace for user-related operations
ns_user = api.namespace('user', description='User operations')


# Define the endpoint to get user points
@ns_user.route('/<address>/points')
@ns_user.param('address', 'The Ethereum address of the user')
class UserPoints(Resource):
    @api.doc(description='Fetch the amount of points for a given Ethereum address from Compound v2')
    @api.marshal_with(points_model)  # Automatically use the points_model for response serialization
    def get(self, address):
        # Validate the address format
        if not web3.is_address(address):
            return {'error': 'Invalid address format'}, 400

        points = 0  # Here you would typically call Compound's smart contract to calculate points

        return {'address': address, 'points': points}


# Add the namespace to the API
api.add_namespace(ns_user)

if __name__ == "__main__":
    app.run(debug=True)  # Set debug to False in production
