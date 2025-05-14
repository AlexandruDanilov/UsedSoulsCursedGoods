import os
import json
from flask import Blueprint, render_template

# Create a Blueprint for the cart API
cart_api = Blueprint('cart_api', __name__)

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

@cart_api.route("/cart")
def cart():
    cart = load_cart()  # Load the cart from cart.json
    total_price = 0
    cart_items = []

    # Load products from products.json
    with open("data/products.json") as f:
        products = json.load(f)

    # Build cart items with product details
    for product_id, quantity in cart.items():
        product = next((p for p in products if p["id"] == int(product_id)), None)
        if product:
            product_total = quantity * product.get("price", 0)
            total_price += product_total
            cart_items.append({
                "id": product_id,
                "name": product["name"],
                "quantity": quantity,
                "price": product["price"],
                "total": product_total
            })

    return render_template("cart.html", cart_items=cart_items, total_price=total_price)