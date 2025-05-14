import os
import json
from flask import Blueprint, request, jsonify

# Create a Blueprint for the add_item API
add_item_api = Blueprint('add_item_api', __name__)

# Path to the cart.json file
CART_FILE = os.path.join("data", "cart.json")

# Helper function to load the cart from cart.json
def load_cart():
    if os.path.exists(CART_FILE):
        with open(CART_FILE, "r") as f:
            return json.load(f)
    return {}

# Helper function to save the cart to cart.json
def save_cart(cart):
    with open(CART_FILE, "w") as f:
        json.dump(cart, f, indent=4)

@add_item_api.route('/cart/add-item', methods=['POST'])
def add_item():
    product_id = request.json.get("id")  # Expecting JSON payload with "id"
    quantity = request.json.get("quantity", 1)  # Default quantity is 1 if not provided

    if product_id:
        cart = load_cart()  # Load the current cart from cart.json
        if quantity > 0:
            # If the item already exists in the cart, increase the quantity
            if product_id in cart:
                cart[product_id] += quantity
            else:
                cart[product_id] = quantity  # Set the quantity for new items
        else:
            cart.pop(product_id, None)  # Remove the item if quantity is zero or less
        save_cart(cart)  # Save the updated cart back to cart.json
        return jsonify({"message": "Item added to cart", "cart": cart}), 200
    return jsonify({"error": "Product ID is required"}), 400