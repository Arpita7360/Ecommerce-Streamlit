
import streamlit as st
import sqlite3
import hashlib
from datetime import datetime
from urllib.parse import quote
from html import escape

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="ShopEase | Online Shopping",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

DB_NAME = "shopease.db"

# --------------------------------------------------
# DATABASE
# --------------------------------------------------
def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users_v2 (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS orders_v2 (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL,
                items TEXT NOT NULL,
                total REAL NOT NULL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        conn.commit()

def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def register_user(name, email, password):
    try:
        with get_connection() as conn:
            conn.execute("""
                INSERT INTO users_v2 (name, email, password_hash, created_at)
                VALUES (?, ?, ?, ?)
            """, (
                name.strip(),
                email.strip().lower(),
                hash_password(password),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ))
            conn.commit()
        return True, "Account created successfully."
    except sqlite3.IntegrityError:
        return False, "An account with this email already exists."

def login_user(email, password):
    with get_connection() as conn:
        row = conn.execute("""
            SELECT name, email FROM users_v2
            WHERE email = ? AND password_hash = ?
        """, (
            email.strip().lower(),
            hash_password(password)
        )).fetchone()
    return row

def save_order(email, items, total):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO orders_v2 (email, items, total, status, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (
            email,
            "\n".join(
                f"{item['name']} x {item['quantity']}"
                for item in items
            ),
            total,
            "Demo order placed",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
        conn.commit()

def get_orders(email):
    with get_connection() as conn:
        return conn.execute("""
            SELECT id, items, total, status, created_at
            FROM orders_v2
            WHERE email = ?
            ORDER BY id DESC
        """, (email,)).fetchall()

init_db()

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
defaults = {
    "user": None,
    "cart": {},
    "wishlist": [],
    "ratings": {},
    "search": "",
    "active_category": "All",
    "auth_page": "Home",
    "last_order": None
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# --------------------------------------------------
# CUSTOM THEME
# --------------------------------------------------
st.markdown("""
<style>
.stApp {
    background: #08090d;
    color: #ffffff;
}
[data-testid="stHeader"] {
    background: rgba(8, 9, 13, 0.95);
}
[data-testid="stSidebar"] {
    background: #11131b;
    border-right: 1px solid #282b38;
}
h1, h2, h3, h4, p, label, li, span {
    color: #ffffff;
}
div[data-testid="stMetric"] {
    background: #171a24;
    border: 1px solid #303448;
    border-radius: 12px;
    padding: 12px;
}
div.stButton > button {
    background: linear-gradient(90deg, #ff416c, #7c4dff);
    color: white;
    border: 0;
    border-radius: 9px;
    font-weight: 600;
    min-height: 38px;
}
div.stButton > button:hover {
    border: 1px solid #ffffff;
    color: #ffffff;
    filter: brightness(1.12);
}
div[data-testid="stForm"] {
    background: #11131b;
    border: 1px solid #303448;
    padding: 18px;
    border-radius: 12px;
}
input, textarea {
    color: #ffffff !important;
}
.product-card {
    background: #11131b;
    border: 1px solid #2a2d3a;
    border-radius: 12px;
    padding: 10px;
    margin-bottom: 8px;
}
.product-name {
    font-weight: 700;
    font-size: 15px;
    min-height: 42px;
    color: #ffffff;
}
.product-price {
    color: #43e6a3;
    font-size: 18px;
    font-weight: 800;
}
.small-muted {
    color: #b8bdce;
    font-size: 12px;
}
.hero {
    background: linear-gradient(120deg, #26104a, #121d39, #391326);
    border: 1px solid #44335f;
    padding: 25px;
    border-radius: 16px;
    margin-bottom: 18px;
}
.hero h1 {
    font-size: 38px;
    margin-bottom: 5px;
}
.hero p {
    color: #e2e5f1;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# PRODUCT CATALOG
# Supports both full URLs and Unsplash photo IDs.
# --------------------------------------------------
products = []

def add_product(category, subcategory, name, price, image, description):
    if image.startswith(("http://", "https://")):
        image_url = image
    else:
        image_url = (
            f"https://images.unsplash.com/{image}"
            "?auto=format&fit=crop&w=700&q=80"
        )

    products.append({
        "id": len(products) + 1,
        "category": category,
        "subcategory": subcategory,
        "name": name,
        "price": float(price),
        "image": image_url,
        "description": description
    })

# --------------------------------------------------
# FASHION
# --------------------------------------------------
fashion_items = [
    ("Men", "Men's Casual Shirt", 799, "photo-1596755094514-f87e34085b2c", "Comfortable casual shirt for everyday wear."),
    ("Men", "Men's T-Shirt", 399, "photo-1521572163474-6864f9cf17ab", "Soft everyday cotton T-shirt."),
    ("Men", "Men's Jeans", 999, "photo-1542272604-787c3835535d", "Classic denim jeans."),
    ("Men", "Men's Jacket", 1499, "photo-1551028719-00167b16eac5", "Stylish jacket for casual outfits."),
    ("Men", "Men's Kurta", 899, "photo-1598033129183-c4f50c736f10", "Traditional kurta for special occasions."),
    ("Men", "Men's Blazer", 1999, "photo-1591047139829-d91aecb6caea", "Smart blazer for formal occasions."),
    ("Women", "Women's Kurti", 699, "photo-1583391733956-6c78276477e7", "Everyday ethnic kurti."),
    ("Women", "Women's Jeans", 999, "photo-1541099649105-f69ad21f3246", "Modern denim jeans."),
    ("Women", "Women's Crop Top", 449, "photo-1503342217505-b0a15ec3261c", "Trendy crop top."),
    ("Women", "Bodycon Dress", 1199, "photo-1539008835657-9e8e9680c956", "Fitted party dress."),
    ("Women", "Women's Saree", 1499, "photo-1610030469983-98e550d6193c", "Traditional saree for celebrations."),
    ("Women", "Lehenga", 2499, "photo-1583391733956-6c78276477e7", "Festive ethnic lehenga."),
    ("Women", "Anarkali Gown", 1899, "photo-1595777457583-95e059d581b8", "Elegant Anarkali-style occasion wear.")
]
for subcategory, name, price, image, description in fashion_items:
    add_product("Fashion", subcategory, name, price, image, description)

# --------------------------------------------------
# MOBILES
# --------------------------------------------------
mobile_items = [
    ("Samsung", "Samsung Galaxy Smartphone", 18999, "photo-1511707171634-5f897ff02aa9"),
    ("Vivo", "Vivo Smartphone", 14999, "photo-1598327105666-5b89351aff97"),
    ("Oppo", "Oppo Smartphone", 15999, "photo-1511707171634-5f897ff02aa9"),
    ("Realme", "Realme Smartphone", 12999, "photo-1598327105666-5b89351aff97"),
    ("iPhone", "Apple iPhone", 59999, "photo-1592899677977-9c10ca588bbd"),
    ("Motorola", "Motorola Smartphone", 16999, "photo-1511707171634-5f897ff02aa9")
]
for brand, name, price, image in mobile_items:
    add_product("Mobiles", brand, name, price, image, f"{brand} smartphone. Check the seller's specifications before purchase.")

# --------------------------------------------------
# ELECTRONICS
# --------------------------------------------------
electronics_items = [
    ("Laptop", 45999, "photo-1496181133206-80ce9b88a853", "Laptop for work, study, and entertainment."),
    ("Monitor", 11999, "photo-1527443224154-c4a3942d3acf", "Desktop monitor for home or office."),
    ("Printer", 7999, "photo-1612815154858-60aa4c59eaa6", "Printer for documents and everyday tasks."),
    ("Projector", 18999, "photo-1574717024653-61fd2cf4d44d", "Projector for presentations and home viewing.")
]
for name, price, image, description in electronics_items:
    add_product("Electronics", name, name, price, image, description)

# --------------------------------------------------
# ACCESSORIES
# --------------------------------------------------
accessory_items = [
    ("Men's Watch", 1299, "photo-1524592094714-0f0654e20314", "Stylish wristwatch."),
    ("Women's Watch", 1599, "photo-1523275335684-37898b6baf30", "Elegant wristwatch."),
    ("Sunglasses", 699, "photo-1511499767150-a48a237f0083", "Fashion sunglasses."),
    ("Earrings", 399, "photo-1535632066927-ab7c9ab60908", "Decorative earrings."),
    ("Keychain", 149, "photo-1617038220319-276d3cfab638", "Small everyday keychain."),
    ("Necklace Set", 999, "photo-1599643478518-a784e5dc4c8f", "Necklace set for special occasions."),
    ("Rings", 499, "photo-1605100804763-247f67b3557e", "Fashion rings.")
]
for name, price, image, description in accessory_items:
    add_product("Accessories", name, name, price, image, description)

# --------------------------------------------------
# TOYS
# --------------------------------------------------
toy_items = [
    ("Teddy Bear", 499, "photo-1559454403-b8fb88521f11"),
    ("Toy Car", 299, "photo-1594787318286-3d835c1d207f"),
    ("Building Blocks", 599, "photo-1587654780291-39c9404d746b"),
    ("Doll", 699, "photo-1560961911-ba7ef651a56c"),
    ("Toy Train", 799, "photo-1516627145497-ae6968895b74"),
    ("Puzzle Game", 349, "photo-1606503153255-59d8b8b821f4"),
    ("Remote Control Car", 1299, "photo-1594787318286-3d835c1d207f"),
    ("Robot Toy", 999, "photo-1535378620166-273708d44e4c"),
    ("Basketball", 499, "photo-1519861531473-9200262188bf"),
    ("Stuffed Animal", 449, "photo-1559454403-b8fb88521f11")
]
for name, price, image in toy_items:
    add_product("Toys", name, name, price, image, f"{name} for play and gifting. Check age suitability before purchase.")

# --------------------------------------------------
# FOOD & HEALTHCARE
# --------------------------------------------------
food_items = [
    ("Almonds (Badam)", 499, "https://images.unsplash.com/photo-1508061253366-f7da158b6d46?auto=format&fit=crop&w=700&q=80", "Crunchy almonds."),
    ("Cashew Nuts (Kaju)", 599, "https://images.unsplash.com/photo-1505576633757-0ac1084af824?auto=format&fit=crop&w=700&q=80", "Creamy cashew nuts."),
    ("Pistachios (Pista)", 549, "https://images.unsplash.com/photo-1511497584788-876760111969?auto=format&fit=crop&w=700&q=80", "Pistachio nuts."),
    ("Walnuts (Akhrot)", 499, "https://images.unsplash.com/photo-1508061253366-f7da158b6d46?auto=format&fit=crop&w=700&q=80", "Walnut kernels."),
    ("Dates (Khajoor)", 349, "https://images.unsplash.com/photo-1559181567-c3190ca9959b?auto=format&fit=crop&w=700&q=80", "Sweet dried dates."),
    ("Dark Chocolate", 249, "https://cdn.gutekueche.de/media/article/72988/conv/schokolade-default.jpg", "Dark chocolate bars."),
    ("Milk Chocolate", 199, "https://resources.koha.net/images/2026/March/23/0a4b309d-10f6-4675-bbdc-30fd4348c113.webp?q=90&r=fill&w=1200", "Milk chocolate pieces.")
]
for name, price, image, description in food_items:
    add_product("Food & Healthcare", "Food", name, price, image, description)

seed_items = [
    ("Chia Seeds", 199),
    ("Flax Seeds (Alsi)", 149),
    ("Pumpkin Seeds", 249),
    ("Sunflower Seeds", 179),
    ("Sesame Seeds (Til)", 129),
    ("Watermelon Seeds", 199),
    ("Basil Seeds (Sabja)", 149),
    ("Hemp Seeds", 299)
]
seed_image = "https://buynutslane.com/cdn/shop/files/SEED_MIX_5.jpg?v=1724921656&width=1200"
for name, price in seed_items:
    add_product(
        "Food & Healthcare", "Seeds", name, price, seed_image,
        f"{name}. Review package details and allergy information."
    )

# --------------------------------------------------
# HELPERS
# --------------------------------------------------
def money(amount):
    return f"₹{amount:,.2f}"

def get_product(product_id):
    return next((p for p in products if p["id"] == product_id), None)

def cart_count():
    return sum(st.session_state.cart.values())

def cart_total():
    total = 0
    for product_id, quantity in st.session_state.cart.items():
        product = get_product(product_id)
        if product:
            total += product["price"] * quantity
    return total

def add_to_cart(product_id):
    st.session_state.cart[product_id] = (
        st.session_state.cart.get(product_id, 0) + 1
    )

def set_quantity(product_id, quantity):
    if quantity <= 0:
        st.session_state.cart.pop(product_id, None)
    else:
        st.session_state.cart[product_id] = quantity

def product_rating(product_id):
    ratings = st.session_state.ratings.get(product_id, [])
    if not ratings:
        return "☆☆☆☆☆", "No ratings yet"
    average = sum(ratings) / len(ratings)
    return "★" * round(average) + "☆" * (5 - round(average)), f"{average:.1f}/5 ({len(ratings)})"

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
with st.sidebar:
    st.markdown("# 🛍️ ShopEase")
    st.caption("Your everyday shopping destination")

    page = st.radio(
        "Navigate",
        [
            "Home", "Shop All", "Fashion", "Mobiles",
            "Electronics", "Accessories", "Toys",
            "Food & Healthcare", "Wishlist", "Cart",
            "My Orders", "Account"
        ],
        key="navigation"
    )

    st.markdown("---")
    st.markdown(f"🛒 **Cart:** {cart_count()} item(s)")

    if st.session_state.user:
        st.success(f"Signed in as {st.session_state.user['name']}")
        if st.button("Logout", use_container_width=True):
            st.session_state.user = None
            st.rerun()
    else:
        st.info("Log in to save and view your orders.")

# --------------------------------------------------
# HOME / ACCOUNT
# --------------------------------------------------
if page == "Home":
    st.markdown("""
    <div class="hero">
        <h1>Welcome to ShopEase 🛍️</h1>
        <p>Discover fashion, mobiles, electronics, accessories, toys, food and more.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("Products", len(products))
    col2.metric("Categories", len(set(p["category"] for p in products)))
    col3.metric("Shopping", "Easy & Simple")

    st.subheader("Get started")
    left, right = st.columns(2)
    with left:
        st.markdown("### Create an account")
        with st.form("register_home"):
            name = st.text_input("Full name", key="home_reg_name")
            email = st.text_input("Email address", key="home_reg_email")
            password = st.text_input("Password", type="password", key="home_reg_password")
            confirm = st.text_input("Confirm password", type="password")
            submitted = st.form_submit_button("Create Account", use_container_width=True)
            if submitted:
                if not name.strip() or not email.strip() or not password:
                    st.error("Please complete all fields.")
                elif password != confirm:
                    st.error("Passwords do not match.")
                elif len(password) < 6:
                    st.error("Use a password with at least 6 characters.")
                else:
                    ok, message = register_user(name, email, password)
                    if ok:
                        st.success(message + " You can now log in from Account.")
                    else:
                        st.error(message)

    with right:
        st.markdown("### Login")
        with st.form("login_home"):
            login_email = st.text_input("Email", key="home_login_email")
            login_password = st.text_input("Password", type="password", key="home_login_password")
            login_submit = st.form_submit_button("Login", use_container_width=True)
            if login_submit:
                user = login_user(login_email, login_password)
                if user:
                    st.session_state.user = {"name": user[0], "email": user[1]}
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Incorrect email or password.")

    st.subheader("Shop by category")
    cols = st.columns(3)
    category_images = {
        "Fashion": "https://images.unsplash.com/photo-1483985988355-763728e1935b?auto=format&fit=crop&w=700&q=80",
        "Mobiles": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=700&q=80",
        "Electronics": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&w=700&q=80",
        "Accessories": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=700&q=80",
        "Toys": "https://images.unsplash.com/photo-1559454403-b8fb88521f11?auto=format&fit=crop&w=700&q=80",
        "Food & Healthcare": seed_image
    }
    categories = list(category_images.keys())
    for i, category in enumerate(categories):
        with cols[i % 3]:
            st.image(category_images[category], use_container_width=True)
            st.markdown(f"**{category}**")
            if st.button(f"Explore {category}", key=f"home_cat_{category}", use_container_width=True):
                st.session_state["navigation"] = category
                st.rerun()

# --------------------------------------------------
# ACCOUNT PAGE
# --------------------------------------------------
elif page == "Account":
    st.title("👤 Account")
    if st.session_state.user:
        st.success(f"Logged in as {st.session_state.user['name']}")
        st.write("Email:", st.session_state.user["email"])
        if st.button("Logout"):
            st.session_state.user = None
            st.rerun()
    else:
        login_tab, register_tab = st.tabs(["Login", "Create Account"])

        with login_tab:
            with st.form("account_login"):
                email = st.text_input("Email", key="account_login_email")
                password = st.text_input("Password", type="password", key="account_login_password")
                submit = st.form_submit_button("Login", use_container_width=True)
                if submit:
                    user = login_user(email, password)
                    if user:
                        st.session_state.user = {"name": user[0], "email": user[1]}
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Incorrect email or password.")

        with register_tab:
            with st.form("account_register"):
                name = st.text_input("Full name", key="account_reg_name")
                email = st.text_input("Email", key="account_reg_email")
                password = st.text_input("Password", type="password", key="account_reg_password")
                confirm = st.text_input("Confirm password", type="password", key="account_reg_confirm")
                submit = st.form_submit_button("Create Account", use_container_width=True)
                if submit:
                    if not name.strip() or not email.strip() or not password:
                        st.error("Please complete all fields.")
                    elif password != confirm:
                        st.error("Passwords do not match.")
                    elif len(password) < 6:
                        st.error("Use a password with at least 6 characters.")
                    else:
                        ok, message = register_user(name, email, password)
                        if ok:
                            st.success(message)
                        else:
                            st.error(message)

# --------------------------------------------------
# SHOP PAGES
# --------------------------------------------------
elif page in [
    "Shop All", "Fashion", "Mobiles", "Electronics",
    "Accessories", "Toys", "Food & Healthcare"
]:
    st.title(f"🛍️ {page}")

    search = st.text_input(
        "🔎 Search products",
        placeholder="Search by product name...",
        key=f"search_{page}"
    )

    col1, col2 = st.columns(2)
    with col1:
        price_limit = st.slider(
            "Maximum price (₹)", 100, 100000, 100000, step=100
        )
    with col2:
        sort_order = st.selectbox(
            "Sort by",
            ["Recommended", "Price: Low to High", "Price: High to Low", "Name"]
        )

    filtered = products[:]
    if page != "Shop All":
        filtered = [p for p in filtered if p["category"] == page]

    if search.strip():
        query = search.strip().lower()
        filtered = [
            p for p in filtered
            if query in p["name"].lower()
            or query in p["category"].lower()
            or query in p["subcategory"].lower()
        ]

    filtered = [p for p in filtered if p["price"] <= price_limit]

    if page == "Fashion":
        fashion_filter = st.radio(
            "Fashion selection",
            ["All", "Men", "Women"],
            horizontal=True
        )
        if fashion_filter != "All":
            filtered = [
                p for p in filtered
                if p["subcategory"] == fashion_filter
            ]

    if page == "Mobiles":
        brands = ["All"] + sorted(set(p["subcategory"] for p in filtered))
        selected_brand = st.selectbox("Mobile brand", brands)
        if selected_brand != "All":
            filtered = [p for p in filtered if p["subcategory"] == selected_brand]

    if page == "Food & Healthcare":
        food_filter = st.radio(
            "Type",
            ["All", "Food", "Seeds"],
            horizontal=True
        )
        if food_filter != "All":
            filtered = [p for p in filtered if p["subcategory"] == food_filter]

    if sort_order == "Price: Low to High":
        filtered.sort(key=lambda p: p["price"])
    elif sort_order == "Price: High to Low":
        filtered.sort(key=lambda p: p["price"], reverse=True)
    elif sort_order == "Name":
        filtered.sort(key=lambda p: p["name"].lower())

    st.caption(f"{len(filtered)} product(s) found")

    if not filtered:
        st.warning("No products match your search and filters.")
    else:
        grid = st.columns(4)
        for i, product in enumerate(filtered):
            with grid[i % 4]:
                with st.container(border=True):
                    st.image(
                        product["image"],
                        use_container_width=True,
                        output_format="auto"
                    )
                    st.markdown(
                        f"<div class='product-name'>{escape(product['name'])}</div>",
                        unsafe_allow_html=True
                    )
                    st.markdown(
                        f"<div class='product-price'>{money(product['price'])}</div>",
                        unsafe_allow_html=True
                    )
                    stars, rating_text = product_rating(product["id"])
                    st.caption(f"{stars}  {rating_text}")
                    st.caption(product["description"])

                    with st.popover("⭐ Rate product", use_container_width=True):
                        rating = st.select_slider(
                            "Your rating",
                            options=[1, 2, 3, 4, 5],
                            value=5,
                            key=f"rating_{product['id']}"
                        )
                        if st.button("Submit rating", key=f"rate_btn_{product['id']}"):
                            st.session_state.ratings.setdefault(product["id"], []).append(rating)
                            st.success("Rating saved for this session.")

                    c1, c2 = st.columns(2)
                    with c1:
                        if st.button("🛒 Add", key=f"add_{product['id']}", use_container_width=True):
                            add_to_cart(product["id"])
                            st.toast(f"{product['name']} added to cart!")
                    with c2:
                        is_saved = product["id"] in st.session_state.wishlist
                        label = "❤️ Saved" if is_saved else "♡ Save"
                        if st.button(label, key=f"wish_{product['id']}", use_container_width=True):
                            if is_saved:
                                st.session_state.wishlist.remove(product["id"])
                            else:
                                st.session_state.wishlist.append(product["id"])
                            st.rerun()

# --------------------------------------------------
# WISHLIST
# --------------------------------------------------
elif page == "Wishlist":
    st.title("❤️ My Wishlist")
    saved_products = [
        get_product(pid) for pid in st.session_state.wishlist
        if get_product(pid)
    ]
    if not saved_products:
        st.info("Your wishlist is empty. Save products while shopping.")
    else:
        for product in saved_products:
            with st.container(border=True):
                c1, c2, c3 = st.columns([1, 3, 1])
                with c1:
                    st.image(product["image"], use_container_width=True)
                with c2:
                    st.subheader(product["name"])
                    st.write(money(product["price"]))
                    st.caption(product["description"])
                with c3:
                    if st.button("Add to cart", key=f"wish_add_{product['id']}"):
                        add_to_cart(product["id"])
                        st.toast("Added to cart.")
                    if st.button("Remove", key=f"wish_remove_{product['id']}"):
                        st.session_state.wishlist.remove(product["id"])
                        st.rerun()

# --------------------------------------------------
# CART AND CHECKOUT
# --------------------------------------------------
elif page == "Cart":
    st.title("🛒 Shopping Cart")

    if not st.session_state.cart:
        st.info("Your cart is empty. Add products from the Shop.")
    else:
        for product_id in list(st.session_state.cart.keys()):
            product = get_product(product_id)
            if not product:
                continue
            quantity = st.session_state.cart[product_id]

            with st.container(border=True):
                c1, c2, c3, c4 = st.columns([1, 3, 2, 1])
                with c1:
                    st.image(product["image"], use_container_width=True)
                with c2:
                    st.subheader(product["name"])
                    st.write(money(product["price"]))
                with c3:
                    new_quantity = st.number_input(
                        "Quantity",
                        min_value=0,
                        max_value=99,
                        value=quantity,
                        step=1,
                        key=f"qty_{product_id}"
                    )
                    if new_quantity != quantity:
                        set_quantity(product_id, new_quantity)
                        st.rerun()
                with c4:
                    st.write("Subtotal")
                    st.write(money(product["price"] * quantity))

        st.markdown("---")
        total = cart_total()
        st.subheader(f"Total: {money(total)}")

        st.markdown("### Checkout details")
        with st.form("checkout_form"):
            full_name = st.text_input(
                "Full name",
                value=st.session_state.user["name"] if st.session_state.user else ""
            )
            address = st.text_area("Delivery address")
            phone = st.text_input("Phone number")
            payment = st.selectbox(
                "Payment method",
                ["Cash on Delivery (Demo)", "UPI (Demo)", "Card (Demo)"]
            )
            place_order = st.form_submit_button("Place Demo Order", use_container_width=True)

            if place_order:
                if not st.session_state.user:
                    st.error("Please create an account and log in before placing an order.")
                elif not full_name.strip() or not address.strip() or not phone.strip():
                    st.error("Please enter your name, delivery address, and phone number.")
                elif len(phone.strip()) < 10:
                    st.error("Please enter a valid phone number.")
                else:
                    order_items = []
                    for product_id, quantity in st.session_state.cart.items():
                        product = get_product(product_id)
                        if product:
                            order_items.append({
                                "name": product["name"],
                                "quantity": quantity
                            })
                    save_order(
                        st.session_state.user["email"],
                        order_items,
                        total
                    )
                    st.session_state.last_order = {
                        "total": total,
                        "payment": payment,
                        "name": full_name.strip()
                    }
                    st.session_state.cart = {}
                    st.success("Demo order placed successfully!")
                    st.info(
                        "This is a demonstration checkout. No payment was processed "
                        "and no delivery service was contacted."
                    )
                    st.rerun()

    if st.session_state.last_order:
        st.markdown("---")
        st.success("Your latest demo order")
        st.write("Customer:", st.session_state.last_order["name"])
        st.write("Total:", money(st.session_state.last_order["total"]))
        st.write("Payment option:", st.session_state.last_order["payment"])

# --------------------------------------------------
# ORDER HISTORY
# --------------------------------------------------
elif page == "My Orders":
    st.title("📦 My Orders")
    if not st.session_state.user:
        st.warning("Please log in to view your orders.")
    else:
        orders = get_orders(st.session_state.user["email"])
        if not orders:
            st.info("You have not placed any orders yet.")
        else:
            for order in orders:
                order_id, items, total, status, created_at = order
                with st.expander(f"Order #{order_id} — {money(total)} — {created_at}"):
                    st.write("Items:")
                    st.code(items)
                    st.write("Status:", status)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown("---")
st.markdown(
    "<p style='text-align:center;color:#aab0c0;'>"
    "© ShopEase | Educational e-commerce demo"
    "</p>",
    unsafe_allow_html=True
)
