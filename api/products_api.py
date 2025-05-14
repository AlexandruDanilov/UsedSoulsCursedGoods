import json
from flask import Blueprint, jsonify

# Create a Blueprint for the API
api = Blueprint('api', __name__)

# Define the products endpoint
@api.route('/api/products', methods=['GET'])
def get_products():
    # Load products from the JSON file
    with open('data/products.json') as f:
        products = json.load(f)
    return jsonify(products)