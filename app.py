
import streamlit as st
import sqlite3
import hashlib
import pandas as pd
from urllib.parse import quote

st.set_page_config(
    page_title="ShopEase | Online Shopping",
    page_icon="🛍️",
    layout="wide"
)

# -------------------- COLOURFUL BLACK THEME --------------------
st.markdown("""
<style>
.stApp {
    background: #080808;
    color: #ffffff;
}
[data-testid="stSidebar"] {
    background: #111111;
    border-right: 1px solid #333333;
}
h1, h2, h3, h4, p, label, span, div {
    color: #ffffff;
}
h1 {
    background: linear-gradient(90deg,#ff4d6d,#ffbe0b,#8338ec,#3a86ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
div.stButton > button,
div.stFormSubmitButton > button {
    background: linear-gradient(90deg,#ff4d6d,#8338ec);
    color: white !important;
    border: none;
    border-radius: 8px;
    font-weight: bold;
}
input, textarea {
    background-color: #202020 !important;
    color: white !important;
}
div[data-testid="stSelectbox"] > div,
div[data-testid="stNumberInput"] > div {
    background: #202020;
    color: white;
}
.product-card {
    background: #151515;
    border: 1px solid #333333;
    border-radius: 10px;
    padding: 10px;
    margin-bottom: 8px;
}
.small-text {
    font-size: 13px;
    color: #bbbbbb;
}
.hero {
    background: linear-gradient(120deg,#391047,#15152e,#073b4c);
    border: 1px solid #5a356a;
    border-radius: 14px;
    padding: 22px;
    margin-bottom: 18px;
}
</style>
""", unsafe_allow_html=True)

# -------------------- DATABASE --------------------
db = sqlite3.connect("shopease.db", check_same_thread=False)
db.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL
)
""")
db.commit()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# -------------------- PRODUCT IMAGES --------------------
# These are real online photography URLs. Internet access is required.
def photo(photo_id):
    return (
        "https://images.unsplash.com/" + photo_id
        + "?auto=format&fit=crop&w=700&q=80"
    )

products = []

def add(category, subcategory, name, price, photo_id, description):
    products.append({
        "id": len(products) + 1,
        "category": category,
        "subcategory": subcategory,
        "name": name,
        "price": price,
        "image": photo(photo_id),
        "description": description
    })

# -------------------- MEN'S FASHION --------------------
men = [
    ("Shirt", 699, "photo-1596755094514-f87e34085b2c"),
    ("T-Shirt", 399, "photo-1521572163474-6864f9cf17ab"),
    ("Jeans", 899, "photo-1542272604-787c3835535d"),
    ("Jacket", 1499, "photo-1551028719-00167b16eac5"),
    ("Kurta", 799, "photo-1598033129183-c4f50c736f10"),
    ("Blazer", 1899, "photo-1591047139829-d91aecb6caea")
]
for name, price, img in men:
    add("Fashion", "Men", name, price, img,
        f"Stylish men's {name.lower()} for everyday wear and special occasions.")

# -------------------- WOMEN'S FASHION --------------------
women = [
    ("Kurties", 699, "photo-1583391733956-6c78276477e9"),
    ("Jeans", 899, "photo-1541099649105-f69ad21f3246"),
    ("Crop Top", 499, "photo-1551488831-00ddcb6c6bd3"),
    ("Bodycon Dress", 1199, "photo-1539008835657-9e8e9680c956"),
    ("Saree", 1499, "photo-1610030469983-98e550d6193c"),
    ("Lehenga", 2499, "photo-1583391733981-849840f4f8c7"),
    ("Anarkali Gown", 1999, "photo-1595777457583-95e059d581b8")
]
for name, price, img in women:
    add("Fashion", "Women", name, price, img,
        f"Elegant women's {name.lower()} collection.")

# -------------------- MOBILES --------------------
mobiles = [
    ("Samsung", 15999, "photo-1511707171634-5f897ff02aa9"),
    ("Vivo", 12999, "photo-1598327105666-5b89351aff97"),
    ("Oppo", 13999, "photo-1598327105666-5b89351aff97"),
    ("Realme", 11999, "photo-1511707171634-5f897ff02aa9"),
    ("iPhone", 59999, "photo-1592750475338-74b7b21085ab"),
    ("Motorola", 14999, "photo-1598327105666-5b89351aff97")
]
for name, price, img in mobiles:
    add("Mobiles", name, name + " Smartphone", price, img,
        f"{name} smartphone. Check the seller's specifications before purchase.")

# -------------------- ELECTRONICS --------------------
electronics = [
    ("Laptop", 45999, "photo-1496181133206-80ce9b88a853"),
    ("Monitor", 12999, "photo-1527443224154-c4a3942d3acf"),
    ("Printer", 8999, "photo-1612815154858-60aa4c59eaa6"),
    ("Projector", 18999, "photo-1528395874238-34ebe249b3f2")
]
for name, price, img in electronics:
    add("Electronics", "Electronics", name, price, img,
        f"{name} for your home, study, or office setup.")

# -------------------- ACCESSORIES --------------------
accessories = [
    ("Men's Watch", 1299, "photo-1523275335684-37898b6baf30"),
    ("Women's Watch", 1599, "photo-1524592094714-0f0654e20314"),
    ("Sunglasses", 599, "photo-1511499767150-a48a237f0083"),
    ("Earrings", 299, "photo-1535632066927-ab7c9ab60908"),
    ("Keychain", 149, "photo-1611652022419-a9419f74343d"),
    ("Necklace Set", 799, "photo-1599643478518-a784e5dc4c8f"),
    ("Rings", 399, "photo-1605100804763-247f67b3557e")
]
for name, price, img in accessories:
    add("Accessories", "Accessories", name, price, img,
        f"Trendy {name.lower()} to complete your look.")

# -------------------- 10 TYPES OF TOYS --------------------
toys = [
    ("Teddy Bear", 499, "photo-1559454403-b8fb88521f11"),
    ("Toy Car", 299, "photo-1594787318286-3d835c1d207f"),
    ("Building Blocks", 599, "photo-1587654780291-39c9404d746b"),
    ("Doll", 399, "photo-1599629954294-14df9ec8f6b7"),
    ("Toy Train", 699, "photo-1516627145497-ae6968895b74"),
    ("Puzzle Game", 249, "photo-1606503153255-59d8b8b821f8"),
    ("Remote Control Car", 999, "photo-1594787318286-3d835c1d207f"),
    ("Robot Toy", 799, "photo-1535378620166-273708d44e4c"),
    ("Soft Ball", 199, "photo-1579952363873-27f3bade9f55"),
    ("Toy Kitchen Set", 899, "photo-1596461404969-9ae70f2830c1")
]
for name, price, img in toys:
    add("Toys", "Toys", name, price, img,
        f"{name} for playtime and gifting. Check the recommended age before buying.")

# -------------------- FOOD & HEALTHCARE --------------------
food = [
    ("Almonds", 499, "photo-1508061253366-f7da158b6d46"),
    ("Cashew Nuts", 599, "photo-1601593768795-6d4e6f1b9a2e"),
    ("Pistachios", 549, "photo-1505576633757-0ac1084af824"),
    ("Walnuts", 499, "photo-1511497584788-876760111969"),
    ("Dates", 349, "photo-1559181567-c3190ca9959b"),
    ("Dark Chocolate", 249, "photo-1548907040-4d42baa9c5a3"),
    ("Milk Chocolate", 199, "photo-1511381939415-e44015466834")
]
for name, price, img in food:
    add("Food & Healthcare", "Food", name, price, img,
        f"Packaged {name.lower()}. Check the label, ingredients, and expiry date.")

seeds = [
    ("Chia Seeds", 199, "photo-1515543904379-3d757afe72e4"),
    ("Flax Seeds", 149, "photo-1603048719539-9ecb4aa395e3"),
    ("Pumpkin Seeds", 249, "photo-1515543904379-3d757afe72e4"),
    ("Sunflower Seeds", 179, "photo-1471943311424-646960669fbc"),
    ("Sesame Seeds", 129, "photo-1603048719539-9ecb4aa395e3"),
    ("Watermelon Seeds", 199, "photo-1515543904379-3d757afe72e4"),
    ("Basil Seeds", 149, "photo-1515543904379-3d757afe72e4"),
    ("Hemp Seeds", 299, "photo-1603048719539-9ecb4aa395e3")
]
for name, price, img in seeds:
    add("Food & Healthcare", "Seeds", name, price, img,
        f"{name} for food use. Review the package and allergy information.")

df = pd.DataFrame(products)

# -------------------- SESSION DATA --------------------
for key, default in {
    "user": None,
    "cart": {},
    "wishlist": [],
    "ratings": {},
    "page": "Home"
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# -------------------- TOP HEADER --------------------
st.markdown("""
<div class="hero">
    <h1>🛍️ ShopEase</h1>
    <h3>Fashion • Mobiles • Electronics • Toys • More</h3>
    <p>Discover your style. Find your favourites. Shop with ease!</p>
</div>
""", unsafe_allow_html=True)

# -------------------- ACCOUNT HOMEPAGE --------------------
if not st.session_state.user:
    st.subheader("Welcome to ShopEase 👋")
    st.write("Create your account or log in to start shopping.")

    account_tab, login_tab = st.tabs(["✨ Create Account", "🔐 Login"])

    with account_tab:
        with st.form("register_form"):
            new_user = st.text_input("Create username")
            new_pass = st.text_input("Create password", type="password")
            confirm_pass = st.text_input("Confirm password", type="password")
            register = st.form_submit_button("Create Account")
        if register:
            if not new_user.strip() or not new_pass:
                st.error("Please enter a username and password.")
            elif new_pass != confirm_pass:
                st.error("Passwords do not match.")
            else:
                try:
                    db.execute(
                        "INSERT INTO users VALUES (?, ?)",
                        (new_user.strip(), hash_password(new_pass))
                    )
                    db.commit()
                    st.success("Account created! Please log in.")
                except sqlite3.IntegrityError:
                    st.error("This username already exists.")

    with login_tab:
        with st.form("login_form"):
            username = st.text_input("Username", key="login_user")
            password = st.text_input("Password", type="password", key="login_pass")
            login = st.form_submit_button("Login")
        if login:
            record = db.execute(
                "SELECT password FROM users WHERE username = ?",
                (username.strip(),)
            ).fetchone()
            if record and record[0] == hash_password(password):
                st.session_state.user = username.strip()
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Incorrect username or password.")

    st.markdown("---")
    st.subheader("🌈 Explore Our Collections")
    st.write("Fashion | Mobiles | Electronics | Accessories | Toys | Food & Healthcare")
    st.caption("Create an account or log in to access your shopping cart and wishlist.")
    st.stop()

# -------------------- SIDEBAR NAVIGATION --------------------
st.sidebar.title("🛍️ ShopEase")
st.sidebar.success("Logged in as " + st.session_state.user)

page = st.sidebar.radio(
    "Navigate",
    ["Home", "Fashion", "Mobiles", "Electronics", "Accessories",
     "Toys", "Food & Healthcare", "Wishlist", "Cart", "My Orders"],
    key="navigation"
)
if st.sidebar.button("Logout"):
    st.session_state.user = None
    st.rerun()

# -------------------- HOME --------------------
if page == "Home":
    st.subheader("✨ Shop by Category")
    category_cols = st.columns(3)
    category_names = [
        "Fashion", "Mobiles", "Electronics",
        "Accessories", "Toys", "Food & Healthcare"
    ]
    for i, cat in enumerate(category_names):
        with category_cols[i % 3]:
            st.markdown('<div class="product-card">', unsafe_allow_html=True)
            st.subheader(cat)
            st.write({
                "Fashion": "👕 Men & Women",
                "Mobiles": "📱 Popular brands",
                "Electronics": "💻 Devices & office",
                "Accessories": "⌚ Style essentials",
                "Toys": "🧸 Fun for kids",
                "Food & Healthcare": "🥜 Dry fruits, chocolate & seeds"
            }[cat])
            if st.button("Explore " + cat, key="explore_" + cat):
                st.session_state["selected_category"] = cat
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

    st.subheader("🔥 Popular Products")
    view = df.head(6)
    cols = st.columns(3)
    for i, (_, p) in enumerate(view.iterrows()):
        with cols[i % 3]:
            st.image(p["image"], use_container_width=True)
            st.write("**" + p["name"] + "**")
            st.write(f"₹{p['price']:,}")
            if st.button("Add to Cart", key=f"home_cart_{p['id']}"):
                st.session_state.cart[p["id"]] = st.session_state.cart.get(p["id"], 0) + 1
                st.success("Added to cart!")

# -------------------- PRODUCT CATALOGUES --------------------
catalogue_pages = [
    "Fashion", "Mobiles", "Electronics", "Accessories",
    "Toys", "Food & Healthcare"
]

if page in catalogue_pages or (
    page == "Home" and st.session_state.get("selected_category") in catalogue_pages
):
    category = (
        st.session_state.get("selected_category")
        if page == "Home" else page
    )
    st.subheader("🛒 " + category)

    search = st.text_input("🔎 Search products", key="search_" + category)
    view = df[df["category"] == category].copy()

    if category == "Fashion":
        audience = st.selectbox("Choose collection", ["All", "Men", "Women"])
        if audience != "All":
            view = view[view["subcategory"] == audience]
    elif category == "Food & Healthcare":
        food_type = st.selectbox("Choose type", ["All", "Food", "Seeds"])
        if food_type != "All":
            view = view[view["subcategory"] == food_type]
    elif category == "Mobiles":
        brand = st.selectbox("Choose brand", ["All"] + sorted(view["subcategory"].unique()))
        if brand != "All":
            view = view[view["subcategory"] == brand]

    if search:
        view = view[view["name"].str.contains(search, case=False, na=False)]

    if view.empty:
        st.info("No products found.")
    else:
        cols = st.columns(3)
        for i, (_, p) in enumerate(view.iterrows()):
            with cols[i % 3]:
                st.markdown('<div class="product-card">', unsafe_allow_html=True)
                st.image(p["image"], use_container_width=True)
                st.write("**" + p["name"] + "**")
                st.write(f"₹{p['price']:,}")
                st.caption(p["description"])

                rating_values = st.session_state.ratings.get(p["id"], [])
                average = sum(rating_values) / len(rating_values) if rating_values else 0
                st.caption(
                    f"⭐ {average:.1f}/5 ({len(rating_values)} ratings)"
                    if rating_values else "⭐ No ratings yet"
                )

                with st.expander("Rate this product"):
                    stars = st.select_slider(
                        "Your rating",
                        options=[1, 2, 3, 4, 5],
                        value=5,
                        key=f"rate_{p['id']}"
                    )
                    if st.button("Submit Rating", key=f"submit_rate_{p['id']}"):
                        st.session_state.ratings.setdefault(p["id"], []).append(stars)
                        st.success("Thank you for rating!")
                        st.rerun()

                if st.button("🛒 Add to Cart", key=f"cart_{p['id']}"):
                    st.session_state.cart[p["id"]] = (
                        st.session_state.cart.get(p["id"], 0) + 1
                    )
                    st.success("Added to cart!")

                if st.button("💜 Add to Wishlist", key=f"wish_{p['id']}"):
                    if p["id"] not in st.session_state.wishlist:
                        st.session_state.wishlist.append(p["id"])
                    st.success("Added to wishlist!")

                st.markdown("</div>", unsafe_allow_html=True)

# -------------------- WISHLIST --------------------
if page == "Wishlist":
    st.subheader("💜 My Wishlist")
    wish_df = df[df["id"].isin(st.session_state.wishlist)]
    if wish_df.empty:
        st.info("Your wishlist is empty.")
    for _, p in wish_df.iterrows():
        c1, c2 = st.columns([1, 3])
        with c1:
            st.image(p["image"], use_container_width=True)
        with c2:
            st.write("**" + p["name"] + "**")
            st.write(f"₹{p['price']:,}")
            if st.button("Add to Cart", key=f"wish_cart_{p['id']}"):
                st.session_state.cart[p["id"]] = st.session_state.cart.get(p["id"], 0) + 1
                st.success("Added to cart!")
            if st.button("Remove", key=f"remove_wish_{p['id']}"):
                st.session_state.wishlist.remove(p["id"])
                st.rerun()

# -------------------- CART & CHECKOUT --------------------
if page == "Cart":
    st.subheader("🛒 My Shopping Cart")
    cart_items = df[df["id"].isin(st.session_state.cart.keys())]
    total = 0

    if cart_items.empty:
        st.info("Your cart is empty. Explore products to start shopping.")
    else:
        for _, p in cart_items.iterrows():
            pid = int(p["id"])
            c1, c2, c3 = st.columns([2, 3, 2])
            with c1:
                st.image(p["image"], use_container_width=True)
            with c2:
                st.write("**" + p["name"] + "**")
                st.write(f"₹{p['price']:,} each")
            with c3:
                qty = st.number_input(
                    "Quantity", min_value=1, max_value=99,
                    value=st.session_state.cart[pid], key=f"qty_{pid}"
                )
                st.session_state.cart[pid] = int(qty)
                if st.button("Remove", key=f"remove_cart_{pid}"):
                    del st.session_state.cart[pid]
                    st.rerun()
            total += p["price"] * st.session_state.cart[pid]

        st.markdown("---")
        st.subheader(f"Total: ₹{total:,}")

        with st.form("checkout_form"):
            st.subheader("📦 Delivery Details")
            customer_name = st.text_input("Full name")
            phone = st.text_input("Phone number")
            address = st.text_area("Full delivery address")
            payment = st.selectbox(
                "Payment method",
                ["Cash on Delivery", "UPI Demo", "Card Demo"]
            )
            place_order = st.form_submit_button("Place Order")

        if place_order:
            if not customer_name.strip() or not phone.strip() or not address.strip():
                st.error("Please fill in all delivery details.")
            else:
                order = {
                    "username": st.session_state.user,
                    "items": [
                        {
                            "name": p["name"],
                            "quantity": st.session_state.cart[int(p["id"])],
                            "price": p["price"]
                        }
                        for _, p in cart_items.iterrows()
                    ],
                    "total": total,
                    "payment": payment,
                    "customer": customer_name,
                    "phone": phone,
                    "address": address
                }
                st.session_state.setdefault("orders", []).append(order)
                st.session_state.cart = {}
                st.session_state["latest_order"] = order
                st.session_state["show_order_confirmation"] = True
                st.rerun()

# -------------------- ORDER CONFIRMATION --------------------
if st.session_state.get("show_order_confirmation", False):
    order = st.session_state.get("latest_order")
    if order and order["username"] == st.session_state.user:
        st.success("🎉 Order placed successfully!")
        st.subheader("Order Summary")
        for item in order["items"]:
            st.write(
                f"{item['name']} × {item['quantity']} — "
                f"₹{item['price'] * item['quantity']:,}"
            )
        st.write(f"**Total: ₹{order['total']:,}**")
        st.write("Payment method: " + order["payment"])
        st.write("Delivery to: " + order["customer"])
        if st.button("Continue Shopping"):
            st.session_state["show_order_confirmation"] = False
            st.session_state["page"] = "Home"
            st.rerun()

# -------------------- ORDER HISTORY --------------------
if page == "My Orders":
    st.subheader("📦 My Orders")
    orders = [
        o for o in st.session_state.get("orders", [])
        if o["username"] == st.session_state.user
    ]
    if not orders:
        st.info("You have not placed any orders yet.")
    for i, order in enumerate(reversed(orders), start=1):
        with st.expander(f"Order {i} — ₹{order['total']:,}"):
            for item in order["items"]:
                st.write(f"{item['name']} × {item['quantity']}")
            st.write("Payment: " + order["payment"])
            st.write("Delivery address: " + order["address"])

st.markdown("---")
st.caption("ShopEase demo website • Sample prices • Online images • Demo payments only")
