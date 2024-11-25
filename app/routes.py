from flask_restx import Namespace, Resource, fields
from flask import jsonify
from .models import UserPoints, db
from web3 import Web3
import os
import logging

# Initialize the Web3 connection
infura_url = os.environ.get('INFURA_URL')
web3 = Web3(Web3.HTTPProvider(infura_url))

# Define API namespace
ns_user = Namespace('user', description='User operations')

# Define response model for points
points_model = ns_user.model('Points', {
    'address': fields.String(description='The Ethereum address of the user', required=True),
    'points': fields.Integer(description='The amount of points for the user')
})

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@ns_user.route('/<address>/points')
@ns_user.param('address', 'The Ethereum address of the user')
class UserPointsRoute(Resource):
    @ns_user.doc(description='Fetch the amount of points for a given Ethereum address from Compound v2')
    @ns_user.marshal_with(points_model)  # Serialize the response with points_model
    def get(self, address):
        # Validate Ethereum address format
        if not web3.is_address(address):
            return {'error': 'Invalid address format'}, 400

        # Retrieve user from the database
        user = UserPoints.query.filter_by(address=address).first()

        """
        # Notes:
        # For creating:
        
        from app import db, 
        user = UserPoints(address='0x1234567890abcdef', points=50)
        db.session.add(user)
        db.session.commit()
        UserPoints.query.all()
        """

        if not user:
            # If user does not exist, create a new entry
            user = UserPoints(address=address, points=0)
            db.session.add(user)
            db.session.commit()

        return {'address': address, 'points': user.points}


# Register namespaces
def register_routes(api):
    api.add_namespace(ns_user)