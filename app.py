
import streamlit as st
import sqlite3
import hashlib
import pandas as pd
from datetime import datetime

# =========================================================
# 1. PAGE SETTINGS
# =========================================================
st.set_page_config(
    page_title="ShopEase | Online Shopping",
    page_icon="🛍️",
    layout="wide"
)

# =========================================================
# 2. COLOURFUL BLACK THEME
# =========================================================
st.markdown("""
<style>
.stApp {
    background-color: #080808;
    color: white;
}
[data-testid="stSidebar"] {
    background-color: #111111;
}
h1 {
    background: linear-gradient(90deg,#ff4d6d,#ffbe0b,#8338ec,#3a86ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
h2, h3, h4, p, label, span {
    color: white;
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
div[data-testid="stSelectbox"] {
    color: white;
}
.product-card {
    background-color: #151515;
    border: 1px solid #333333;
    border-radius: 10px;
    padding: 10px;
}
.hero {
    background: linear-gradient(120deg,#391047,#15152e,#073b4c);
    border: 1px solid #5a356a;
    border-radius: 14px;
    padding: 22px;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# 3. DATABASE
# Uses users_v2 to avoid the old users table schema error.
# =========================================================
@st.cache_resource
def get_database():
    connection = sqlite3.connect(
        "shopease.db",
        check_same_thread=False
    )
    connection.execute("""
        CREATE TABLE IF NOT EXISTS users_v2 (
            username TEXT PRIMARY KEY,
            password_hash TEXT NOT NULL
        )
    """)
    connection.commit()
    return connection

db = get_database()

def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

# =========================================================
# 4. PRODUCT CATALOGUE
# =========================================================
products = []

def add_product(category, subcategory, name, price, image_id, description):
    products.append({
        "id": len(products) + 1,
        "category": category,
        "subcategory": subcategory,
        "name": name,
        "price": price,
        "image": (
            f"https://images.unsplash.com/{image_id}"
            "?auto=format&fit=crop&w=700&q=80"
        ),
        "description": description
    })

# ---------------- MEN'S FASHION ----------------
men_items = [
    ("Shirt", 699, "photo-1596755094514-f87e34085b2c"),
    ("T-Shirt", 399, "photo-1521572163474-6864f9cf17ab"),
    ("Jeans", 899, "photo-1542272604-787c3835535d"),
    ("Jacket", 1499, "photo-1551028719-00167b16eac5"),
    ("Kurta", 799, "photo-1598033129183-c4f50c736f10"),
    ("Blazer", 1899, "photo-1591047139829-d91aecb6caea")
]

for name, price, image in men_items:
    add_product(
        "Fashion", "Men", name, price, image,
        f"Men's {name.lower()} collection."
    )

# ---------------- WOMEN'S FASHION ----------------
women_items = [
    ("Kurties", 699, "photo-1583391733956-6c78276477e9"),
    ("Jeans", 899, "photo-1541099649105-f69ad21f3246"),
    ("Crop Top", 499, "photo-1551488831-00ddcb6c6bd3"),
    ("Bodycon Dress", 1199, "photo-1539008835657-9e8e9680c956"),
    ("Saree", 1499, "photo-1610030469983-98e550d6193c"),
    ("Lehenga", 2499, "photo-1583391733981-849840f4f8c7"),
    ("Anarkali Gown", 1999, "photo-1595777457583-95e059d581b8")
]

for name, price, image in women_items:
    add_product(
        "Fashion", "Women", name, price, image,
        f"Women's {name.lower()} collection."
    )

# ---------------- MOBILE BRANDS ----------------
mobile_items = [
    ("Samsung", 15999, "photo-1511707171634-5f897ff02aa9"),
    ("Vivo", 12999, "photo-1598327105666-5b89351aff97"),
    ("Oppo", 13999, "photo-1598327105666-5b89351aff97"),
    ("Realme", 11999, "photo-1511707171634-5f897ff02aa9"),
    ("iPhone", 59999, "photo-1592750475338-74b7b21085ab"),
    ("Motorola", 14999, "photo-1598327105666-5b89351aff97")
]

for name, price, image in mobile_items:
    add_product(
        "Mobiles", name, name + " Smartphone", price, image,
        f"{name} smartphone. Check specifications before purchase."
    )

# ---------------- ELECTRONICS ----------------
electronics_items = [
    ("Laptop", 45999, "photo-1496181133206-80ce9b88a853"),
    ("Monitor", 12999, "photo-1527443224154-c4a3942d3acf"),
    ("Printer", 8999, "photo-1612815154858-60aa4c59eaa6"),
    ("Projector", 18999, "photo-1528395874238-34ebe249b3f2")
]

for name, price, image in electronics_items:
    add_product(
        "Electronics", "Electronics", name, price, image,
        f"{name} for your home, study or office."
    )

# ---------------- ACCESSORIES ----------------
accessory_items = [
    ("Men's Watch", 1299, "photo-1523275335684-37898b6baf30"),
    ("Women's Watch", 1599, "photo-1524592094714-0f0654e20314"),
    ("Sunglasses", 599, "photo-1511499767150-a48a237f0083"),
    ("Earrings", 299, "photo-1535632066927-ab7c9ab60908"),
    ("Keychain", 149, "photo-1611652022419-a9419f74343d"),
    ("Necklace Set", 799, "photo-1599643478518-a784e5dc4c8f"),
    ("Rings", 399, "photo-1605100804763-247f67b3557e")
]

for name, price, image in accessory_items:
    add_product(
        "Accessories", "Accessories", name, price, image,
        f"Stylish {name.lower()} for everyday wear and gifting."
    )

# ---------------- TEN TYPES OF TOYS ----------------
toy_items = [
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

for name, price, image in toy_items:
    add_product(
        "Toys", "Toys", name, price, image,
        f"{name} for playtime and gifting."
    )

# ---------------- FOOD & HEALTHCARE ----------------
food_items = [
    ("Almonds", 499, "photo-1508061253366-f7da158b6d46"),
    ("Cashew Nuts", 599, "photo-1505576633757-0ac1084af824"),
    ("Pistachios", 549, "photo-1511497584788-876760111969"),
    ("Walnuts", 499, "photo-1508061253366-f7da158b6d46"),
    ("Dates", 349, "photo-1559181567-c3190ca9959b"),
    ("Dark Chocolate", 249, "photo-1548907040-4d42baa9c5a3"),
    ("Milk Chocolate", 199, "photo-1511381939415-e44015466834")
]

for name, price, image in food_items:
    add_product(
        "Food & Healthcare", "Food", name, price, image,
        f"Packaged {name.lower()}. Check ingredients and expiry date."
    )

seed_items = [
    ("Chia Seeds", 199, "photo-1515543904379-3d757afe72e4"),
    ("Flax Seeds", 149, "photo-1603048719539-9ecb4aa395e3"),
    ("Pumpkin Seeds", 249, "photo-1515543904379-3d757afe72e4"),
    ("Sunflower Seeds", 179, "photo-1471943311424-646960669fbc"),
    ("Sesame Seeds", 129, "photo-1603048719539-9ecb4aa395e3"),
    ("Watermelon Seeds", 199, "photo-1515543904379-3d757afe72e4"),
    ("Basil Seeds", 149, "photo-1515543904379-3d757afe72e4"),
    ("Hemp Seeds", 299, "photo-1603048719539-9ecb4aa395e3")
]

for name, price, image in seed_items:
    add_product(
        "Food & Healthcare", "Seeds", name, price, image,
        f"{name} for food use. Check the package and allergy information."
    )

df = pd.DataFrame(products)

# =========================================================
# 5. SESSION STATE
# =========================================================
defaults = {
    "user": None,
    "cart": {},
    "wishlist": [],
    "ratings": {},
    "orders": [],
    "last_order": None
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# =========================================================
# 6. WEBSITE HEADER
# =========================================================
st.markdown("""
<div class="hero">
    <h1>🛍️ ShopEase</h1>
    <h3>Fashion • Mobiles • Electronics • Accessories</h3>
    <p>Discover your style. Find your favourites. Shop with ease!</p>
</div>
""", unsafe_allow_html=True)

# =========================================================
# 7. CREATE ACCOUNT AND LOGIN
# =========================================================
if not st.session_state.user:

    tab1, tab2 = st.tabs(["✨ Create Account", "🔐 Login"])

    with tab1:
        st.subheader("Create Your Account")

        with st.form("create_account_form"):
            new_username = st.text_input("Create username")
            new_password = st.text_input(
                "Create password", type="password"
            )
            confirm_password = st.text_input(
                "Confirm password", type="password"
            )
            create_account = st.form_submit_button("Create Account")

        if create_account:
            if not new_username.strip() or not new_password:
                st.error("Please enter a username and password.")

            elif len(new_password) < 6:
                st.error("Password must contain at least 6 characters.")

            elif new_password != confirm_password:
                st.error("Passwords do not match.")

            else:
                try:
                    db.execute(
                        """
                        INSERT INTO users_v2 (username, password_hash)
                        VALUES (?, ?)
                        """,
                        (
                            new_username.strip(),
                            hash_password(new_password)
                        )
                    )
                    db.commit()
                    st.success(
                        "Account created successfully! Please log in."
                    )

                except sqlite3.IntegrityError:
                    st.error(
                        "This username already exists. Choose another."
                    )

                except sqlite3.Error:
                    st.error(
                        "Database problem. Please check the app logs."
                    )

    with tab2:
        st.subheader("Login to ShopEase")

        with st.form("login_form"):
            login_username = st.text_input("Username")
            login_password = st.text_input(
                "Password", type="password"
            )
            login_button = st.form_submit_button("Login")

        if login_button:
            try:
                record = db.execute(
                    """
                    SELECT password_hash FROM users_v2
                    WHERE username = ?
                    """,
                    (login_username.strip(),)
                ).fetchone()

                if (
                    record
                    and record[0] == hash_password(login_password)
                ):
                    st.session_state.user = login_username.strip()
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Incorrect username or password.")

            except sqlite3.Error:
                st.error("Database problem. Please check the app logs.")

    st.markdown("---")
    st.subheader("🌈 Explore ShopEase")
    st.write(
        "👕 Fashion  |  📱 Mobiles  |  💻 Electronics  |  "
        "⌚ Accessories  |  🧸 Toys  |  🥜 Food & Healthcare"
    )
    st.caption("Create an account or log in to start shopping.")
    st.stop()

# =========================================================
# 8. SIDEBAR
# =========================================================
st.sidebar.title("🛍️ ShopEase")
st.sidebar.write("Welcome, " + st.session_state.user + "!")

page = st.sidebar.radio(
    "Choose a page",
    [
        "Home",
        "Fashion",
        "Mobiles",
        "Electronics",
        "Accessories",
        "Toys",
        "Food & Healthcare",
        "Wishlist",
        "Cart",
        "My Orders"
    ]
)

if st.sidebar.button("Logout"):
    st.session_state.user = None
    st.session_state.cart = {}
    st.session_state.wishlist = []
    st.rerun()

# =========================================================
# 9. HOME PAGE
# =========================================================
if page == "Home":
    st.subheader("✨ Shop by Category")

    categories = [
        ("Fashion", "👗", "Men's and women's clothing"),
        ("Mobiles", "📱", "Popular smartphone brands"),
        ("Electronics", "💻", "Laptops and office devices"),
        ("Accessories", "⌚", "Watches and jewellery"),
        ("Toys", "🧸", "Toys and games"),
        ("Food & Healthcare", "🥜", "Dry fruits, chocolate and seeds")
    ]

    cols = st.columns(3)

    for i, (category, emoji, description) in enumerate(categories):
        with cols[i % 3]:
            st.markdown('<div class="product-card">', unsafe_allow_html=True)
            st.subheader(emoji + " " + category)
            st.write(description)
            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("🔥 Popular Products")

    popular = df.head(6)
    cols = st.columns(3)

    for i, (_, p) in enumerate(popular.iterrows()):
        with cols[i % 3]:
            st.image(p["image"], use_container_width=True)
            st.write("**" + p["name"] + "**")
            st.write(f"₹{p['price']:,}")

            if st.button("Add to Cart", key=f"home_add_{p['id']}"):
                pid = int(p["id"])
                st.session_state.cart[pid] = (
                    st.session_state.cart.get(pid, 0) + 1
                )
                st.success("Added to cart!")

# =========================================================
# 10. CATEGORY PAGES
# =========================================================
category_pages = [
    "Fashion", "Mobiles", "Electronics",
    "Accessories", "Toys", "Food & Healthcare"
]

if page in category_pages:
    st.subheader("🛍️ " + page)

    search = st.text_input("🔎 Search products")
    view = df[df["category"] == page].copy()

    if page == "Fashion":
        audience = st.selectbox(
            "Select collection", ["All", "Men", "Women"]
        )
        if audience != "All":
            view = view[view["subcategory"] == audience]

    elif page == "Mobiles":
        brands = ["All"] + sorted(view["subcategory"].unique().tolist())
        brand = st.selectbox("Select mobile brand", brands)
        if brand != "All":
            view = view[view["subcategory"] == brand]

    elif page == "Food & Healthcare":
        food_type = st.selectbox(
            "Select type", ["All", "Food", "Seeds"]
        )
        if food_type != "All":
            view = view[view["subcategory"] == food_type]

    if search:
        view = view[
            view["name"].str.contains(search, case=False, na=False)
        ]

    if view.empty:
        st.info("No products found.")
    else:
        cols = st.columns(3)

        for i, (_, p) in enumerate(view.iterrows()):
            with cols[i % 3]:
                pid = int(p["id"])

                st.markdown(
                    '<div class="product-card">',
                    unsafe_allow_html=True
                )
                st.image(p["image"], use_container_width=True)
                st.write("**" + p["name"] + "**")
                st.write(f"₹{p['price']:,}")
                st.caption(p["description"])

                ratings = st.session_state.ratings.get(pid, [])
                if ratings:
                    avg_rating = sum(ratings) / len(ratings)
                    st.write(
                        f"⭐ {avg_rating:.1f}/5 ({len(ratings)} ratings)"
                    )
                else:
                    st.write("⭐ No ratings yet")

                with st.expander("Rate this product"):
                    rating = st.select_slider(
                        "Your rating",
                        options=[1, 2, 3, 4, 5],
                        value=5,
                        key=f"rating_{pid}"
                    )

                    if st.button(
                        "Submit Rating", key=f"submit_rating_{pid}"
                    ):
                        st.session_state.ratings.setdefault(
                            pid, []
                        ).append(rating)
                        st.success("Thank you for your rating!")
                        st.rerun()

                if st.button("🛒 Add to Cart", key=f"add_{pid}"):
                    st.session_state.cart[pid] = (
                        st.session_state.cart.get(pid, 0) + 1
                    )
                    st.success("Added to cart!")

                if st.button("💜 Add to Wishlist", key=f"wish_{pid}"):
                    if pid not in st.session_state.wishlist:
                        st.session_state.wishlist.append(pid)
                        st.success("Added to wishlist!")
                    else:
                        st.info("Already in your wishlist.")

                st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# 11. WISHLIST
# =========================================================
if page == "Wishlist":
    st.subheader("💜 My Wishlist")

    wish_df = df[df["id"].isin(st.session_state.wishlist)]

    if wish_df.empty:
        st.info("Your wishlist is empty.")

    for _, p in wish_df.iterrows():
        pid = int(p["id"])
        col1, col2 = st.columns([1, 3])

        with col1:
            st.image(p["image"], use_container_width=True)

        with col2:
            st.write("**" + p["name"] + "**")
            st.write(f"₹{p['price']:,}")

            if st.button("Add to Cart", key=f"wish_add_{pid}"):
                st.session_state.cart[pid] = (
                    st.session_state.cart.get(pid, 0) + 1
                )
                st.success("Added to cart!")

            if st.button("Remove", key=f"wish_remove_{pid}"):
                st.session_state.wishlist.remove(pid)
                st.rerun()

# =========================================================
# 12. CART
# =========================================================
if page == "Cart":
    st.subheader("🛒 My Shopping Cart")

    if not st.session_state.cart:
        st.info("Your cart is empty. Start shopping!")

    else:
        total = 0
        cart_items = df[
            df["id"].isin(st.session_state.cart.keys())
        ]

        for _, p in cart_items.iterrows():
            pid = int(p["id"])
            col1, col2, col3 = st.columns([1, 2, 1])

            with col1:
                st.image(p["image"], use_container_width=True)

            with col2:
                st.write("**" + p["name"] + "**")
                st.write(f"Price: ₹{p['price']:,}")

            with col3:
                qty = st.number_input(
                    "Quantity",
                    min_value=1,
                    max_value=99,
                    value=int(st.session_state.cart[pid]),
                    key=f"qty_{pid}"
                )
                st.session_state.cart[pid] = int(qty)

                if st.button("Remove", key=f"remove_{pid}"):
                    del st.session_state.cart[pid]
                    st.rerun()

            total += p["price"] * st.session_state.cart[pid]

        st.markdown("---")
        st.subheader(f"Total: ₹{total:,}")

        with st.form("checkout_form"):
            st.subheader("📦 Delivery Details")

            customer_name = st.text_input("Full name")
            phone = st.text_input("Phone number")
            address = st.text_area("Delivery address")

            payment = st.selectbox(
                "Payment method",
                ["Cash on Delivery", "UPI Demo", "Card Demo"]
            )

            place_order = st.form_submit_button("Place Order")

        if place_order:
            if not customer_name.strip() or not phone.strip() or not address.strip():
                st.error("Please fill in all delivery details.")

            else:
                order_items = []

                for _, p in cart_items.iterrows():
                    pid = int(p["id"])
                    quantity = int(st.session_state.cart[pid])

                    order_items.append({
                        "name": p["name"],
                        "quantity": quantity,
                        "price": int(p["price"])
                    })

                order = {
                    "username": st.session_state.user,
                    "date": datetime.now().strftime("%d-%m-%Y %H:%M"),
                    "items": order_items,
                    "total": total,
                    "payment": payment,
                    "customer": customer_name,
                    "phone": phone,
                    "address": address
                }

                st.session_state.orders.append(order)
                st.session_state.last_order = order
                st.session_state.cart = {}
                st.success("🎉 Order placed successfully!")
                st.rerun()

# =========================================================
# 13. ORDER CONFIRMATION
# =========================================================
if st.session_state.last_order:
    order = st.session_state.last_order

    if order["username"] == st.session_state.user:
        st.subheader("📋 Latest Order Confirmation")
        st.write("Order date:", order["date"])

        for item in order["items"]:
            subtotal = item["price"] * item["quantity"]
            st.write(
                f"{item['name']} × {item['quantity']} = ₹{subtotal:,}"
            )

        st.write(f"**Order total: ₹{order['total']:,}**")
        st.write("Payment method:", order["payment"])

# =========================================================
# 14. ORDER HISTORY
# =========================================================
if page == "My Orders":
    st.subheader("📦 My Orders")

    user_orders = [
        order for order in st.session_state.orders
        if order["username"] == st.session_state.user
    ]

    if not user_orders:
        st.info("You have not placed any orders yet.")

    for number, order in enumerate(reversed(user_orders), start=1):
        with st.expander(
            f"Order {number} | ₹{order['total']:,} | {order['date']}"
        ):
            for item in order["items"]:
                st.write(
                    f"{item['name']} × {item['quantity']} "
                    f"— ₹{item['price'] * item['quantity']:,}"
                )

            st.write("Payment:", order["payment"])
            st.write("Customer:", order["customer"])
            st.write("Address:", order["address"])

# =========================================================
# 15. FOOTER
# =========================================================
st.markdown("---")
st.caption(
    "ShopEase | Demo shopping website | Sample prices | "
    "External product images | Demo payments only"
)
