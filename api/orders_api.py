import json
import os
import uuid
from flask import Blueprint, request, jsonify, session, redirect, url_for
from datetime import datetime

# Create a Blueprint for the orders API
orders_api = Blueprint('orders_api', __name__)

# Path to the orders.json file
ORDERS_FILE = os.path.join("data", "orders.json")
CART_FILE = os.path.join("data", "cart.json")

# Helper function to load orders from orders.json
def load_orders():
    if os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE, "r") as f:
            return json.load(f)
    return []

# Helper function to save orders to orders.json
def save_orders(orders):
    with open(ORDERS_FILE, "w") as f:
        json.dump(orders, f, indent=4)

# Helper function to load cart from cart.json
def load_cart():
    if os.path.exists(CART_FILE):
        with open(CART_FILE, "r") as f:
            return json.load(f)
    return {}

# Helper function to save cart to cart.json
def save_cart(cart):
    with open(CART_FILE, "w") as f:
        json.dump(cart, f, indent=4)

@orders_api.route("/orders", methods=["POST"])
def save_order():
    # Load the cart from cart.json
    cart = load_cart()

    

    # Get form data from the request
    name = request.form.get("name")
    email = request.form.get("email")
    address = request.form.get("address")
    phone = request.form.get("phone")
    payment = request.form.get("payment")
    logged_user = session.get("username")  # Get the logged-in user from the session

    # Validate form data
    if not all([name, email, address, phone, payment]):
        return "Missing required fields", 400

    # Generate a unique order ID
    order_id = str(uuid.uuid4())

    # Load existing orders
    orders = load_orders()

    # Create the new order
    new_order = {
        "id": order_id,
        "cart": cart,
        "account_details": {
            "name": name,
            "email": email,
            "address": address,
            "phone": phone,
            "payment": payment
        },
        "logged_user": logged_user,
        "timestamp": datetime.now().isoformat()
    }

    # Add the new order to the list
    orders.append(new_order)

    # Save the updated orders list
    save_orders(orders)

    # Clear the cart after saving the order
    save_cart({})

    # Redirect to a confirmation page
    return redirect(url_for("confirmation", order_id=order_id))