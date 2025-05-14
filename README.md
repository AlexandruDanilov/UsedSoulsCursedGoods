# Used Souls & Cursed Goods - Store Project

This file provides an overview of the **"Used Souls & Cursed Goods"** online store project — a mystical e-commerce platform with a supernatural theme.

## Supported Users

```

"test": "test123",
"admin": "admin123",
"user": "user123",
"guest": "guest123",

```
Peak security...




## Project Structure

This seems like it will save me a lot of time because I don't lose track so I just copy paste the tree here
and explain briefly:

```
README.md               This documentation file
server.py               Web server
requirements.txt        Required (and not) packages to install
api/                    API endpoints
├── add_item_api.py     Handles adding items to cart
├── cart_api.py         Cart management functionality
├── checkout_api.py     Checkout process handling
├── orders_api.py       Order management
└── products_api.py     Products management
data/                   JSON data storage
├── cart.json           Shopping cart data
├── orders.json         Order history
└── products.json       Product information
public/                 Static assets
├── style.css           Custom CSS
├── bootstrap/          Bootstrap framework files (CSS/JS)
└── images/             Store images
templates/              HTML
├── _base.html          Base template with common elements
├── about.html          About page
├── cart.html           Shopping cart view
├── checkout.html       Checkout form
├── confirmation.html   Order confirmation
├── home.html           Homepage
├── index.html          Product listing
└── login.html          User login form

```

---

## Implementation:

**The page aesthetic and products are meant to make whoever is manually checking this question both their sanity and
mine, but it also made this way more fun to do than I assume was intended.** 

The main structure for this store was taken from labs 3 and 4, this being some sort of
mashup between the two (bootstrap and login page were lab 3 and the JSON work was lab 4).

The first challenge was routing everything correctly so that the buttons point to existing pages.
After the button work was completed, I had to neatly design the pages and products. Most of the images
and texts are GPT-generated but they look cool and I find them funny.

Basically everything that required `JSON` work for persisting data was made using an `API` (see the folder).
I tried to be tidy, there are 3 JSONs: one with the products that can't be affected by the user, the cart that
resets after each purchase and the orders that just gets bigger and bigger the more orders are placed.
This ensures only what matters is being kept. 

As per task requirement the index page is the store one, the homepage is just a brief description
of the store. Pages are labeled pretty self-explanatorily so no need to document them further here.
The `server.py` code was relatively tidy at first but now it's mostly a mess of app routes in no particular order.

Everything I did that is not in the task requirement was because it made sense and added another layer of immersion 
into the website.

Also, the `requirements.txt` file has a lot of useless stuff (some was from idst, others from personal projects) that I
was too lazy to remove

## Testing:

The promised testing script was missing. I tried to do the testing as described in the assignment page; however, I am
a human and not a script, so almost all features were tested by clicking page buttons and not writing stuff in the top bar.
After rigorous testing (not really), I concluded that everything functions as expected, but if you find bugs, keep in mind they 
might actually be features.

## Theme

The site embraces a mystical, supernatural theme with a deep purple color scheme and features fictional, spooky products such as:

- Used souls (lightly damned)  
- DIY haunting kits  
- Bottled screams  
- Cursed artifacts  
- Supernatural potions  
- Emotionally unstable familiars  

## Docker container:

I am writing this before putting it into the container but I really promise that it will be also tested on a totally different system, 
like I will upload it to a private github repo and try it on a freshly installed Ubuntu on a Raspberry Pi to really make sure nothing is
missing. If it does not run it is not my fault...

## Final message:

I really wanted to translate this in latin at the end but somebody might
be actually reading this. Hopefully it was not traumatizing and good enough.
I really had a lot of fun doing this so thanks to whoever came with this idea.
