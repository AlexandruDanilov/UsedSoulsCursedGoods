from flask import Flask, request, render_template, redirect, session, url_for
import os
import json
from werkzeug.utils import secure_filename
from api.products_api import api
from api.add_item_api import add_item_api
from api.cart_api import cart_api
from api.checkout_api import checkout_api
from api.orders_api import orders_api


app = Flask(__name__, static_folder="public")
app.secret_key = "supersecret"


ALLOWED_USERS = {
    "test": "test123",
    "admin": "admin123",
    "user": "user123",
    "guest": "guest123",
}

app.register_blueprint(api)
app.register_blueprint(add_item_api)
app.register_blueprint(cart_api)
app.register_blueprint(checkout_api)
app.register_blueprint(orders_api)

# Initialize the cart in the session
@app.before_request
def initialize_cart():
    if "cart" not in session:
        session["cart"] = {}

def load_cart():
    # Load the cart from cart.json
    if os.path.exists("data/cart.json"):
        with open("data/cart.json") as f:
            return json.load(f)
    return {}

def save_cart(cart):
    # Save the cart to cart.json
    with open("data/cart.json", "w") as f:
        json.dump(cart, f)

@app.route("/")
def index():
    # Load products from the JSON file
    with open("data/products.json") as f:
        products = json.load(f)
    return render_template("index.html", products=products)

@app.route("/home")
def home():
    return render_template("home.html")

# Route to display the cart
@app.route("/cart")
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

# Route to add an item to the cart
@app.route("/cart/add-item", methods=["GET"])
def add_item():
    product_id = request.args.get("id")
    if product_id:
        cart = load_cart()  # Load the cart from cart.json
        # Use the update_quantity route to handle this
        if str(product_id) in cart:
            cart[str(product_id)] += 1  # Increase quantity
        else:
            cart[str(product_id)] = 1  # Add item with quantity 1
        save_cart(cart)  # Save the updated cart back to cart.json
    return redirect(url_for("cart"))

# Route to remove an item from the cart
@app.route("/cart/remove-item", methods=["GET"])
def remove_item():
    product_id = request.args.get("id")
    if product_id:
        cart = load_cart()  # Load the cart from cart.json
        if product_id in cart:
            del cart[product_id]  # Remove the item
            save_cart(cart)  # Save the updated cart back to cart.json
    return redirect(url_for("cart"))

@app.route("/cart/update-quantity/<int:id>", methods=["POST"])
def update_quantity(id):
    action = request.form.get("action")  # Get the action (increase or decrease)
    cart = load_cart()  # Load the cart from cart.json

    if str(id) in cart:
        if action == "increase":
            cart[str(id)] += 1  # Increase the quantity
        elif action == "decrease":
            cart[str(id)] -= 1  # Decrease the quantity
            if cart[str(id)] <= 0:
                del cart[str(id)]  # Remove the item if quantity is 0 or less

    save_cart(cart)  # Save the updated cart back to cart.json
    return redirect(url_for("cart"))

@app.route("/about")
def about():
    return render_template("about.html")
    

@app.route("/checkout")
def checkout():
    cart = load_cart()  # Load the cart from cart.json
    cart_products = []
    total_price = 0  # Initialize total price

    # Load products from products.json
    with open("data/products.json") as f:
        products = json.load(f)

    # Build cart products with details and calculate total price
    for product_id, quantity in cart.items():
        product = next((p for p in products if p["id"] == int(product_id)), None)
        if product:
            subtotal = product["price"] * quantity
            total_price += subtotal  # Add subtotal to total price
            cart_products.append({
                "id": product_id,
                "name": product["name"],
                "description": product["description"],
                "price": product["price"],
                "currency": product.get("currency", "USD"),  # Default to USD if not provided
                "image": product["image"],
                "quantity": quantity,
                "subtotal": subtotal  # Include subtotal for each product
            })

    return render_template("checkout.html", cart_products=cart_products, total_price=total_price)

@app.route("/login", methods=["GET", "POST"])
def login():
    error_msg = ""
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        if username in ALLOWED_USERS and ALLOWED_USERS[username] == password:
            session["authenticated"] = True
            session["username"] = username
            return redirect(url_for("index"))
        else:
            error_msg = "Nomen vel tessera non licita. / Username or password is incorrect."

    return render_template("login.html", error_msg=error_msg)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/confirmation")
def confirmation():
    order_id = request.args.get("order_id")
    
    # Load order data from orders.json
    order_data = {}
    try:
        with open("data/orders.json", "r") as f:
            orders_list = json.load(f)
            # Find the order with matching id
            order = next((o for o in orders_list if o.get("id") == order_id), None)
            if order:
                order_data = order
    except (FileNotFoundError, json.JSONDecodeError):
        # Handle case where file doesn't exist or is invalid JSON
        pass
    
    # Extract name and address from account_details
    account_details = order_data.get("account_details", {})
    name = account_details.get("name", "Unknown")
    address = account_details.get("address", "Unknown")
    payment = account_details.get("payment", "Unknown")
    
    return render_template("confirmation.html", 
                          order_id=order_id,
                          name=name,
                          address=address, payment=payment,)

@app.context_processor
def inject_template_vars():
    return {
        "authenticated": session.get("authenticated", False),
        "username": session.get("username", "")
    }



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

