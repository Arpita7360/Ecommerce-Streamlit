
import sqlite3
import hashlib
import hmac
import secrets
import streamlit as st
import pandas as pd

DB = "shopease_catalog.db"

st.set_page_config(
    page_title="ShopEase | Online Shopping",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------- DESIGN ----------------

st.markdown("""
<style>
    .stApp { background-color: #f8f9fc; }
    .main-title {
        font-size: 38px;
        font-weight: 800;
        color: #26345d;
    }
    .subtitle { color: #6c7280; font-size: 16px; }
    div.stButton > button {
        border-radius: 9px;
        font-weight: 600;
    }
    [data-testid="stMetric"] {
        background: white;
        padding: 14px;
        border: 1px solid #e9eaf0;
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)


# ---------------- PRODUCT CATALOGUE ----------------
# Fields: name, category, subcategory, price, emoji, description, stock

CATALOGUE = [
    # FASHION - MEN
    ("Men's Formal Shirt", "Fashion", "Men", 799, "👔", "Smart formal shirt for work and occasions.", 20),
    ("Men's T-Shirt", "Fashion", "Men", 399, "👕", "Comfortable everyday cotton T-shirt.", 25),
    ("Men's Jeans", "Fashion", "Men", 999, "👖", "Classic denim jeans for everyday style.", 18),
    ("Men's Jacket", "Fashion", "Men", 1499, "🧥", "Stylish jacket for casual outings.", 12),
    ("Men's Kurta", "Fashion", "Men", 899, "🥻", "Traditional kurta for festive occasions.", 15),
    ("Men's Blazer", "Fashion", "Men", 1999, "🤵", "Elegant blazer for formal events.", 10),

    # FASHION - WOMEN
    ("Women's Kurti", "Fashion", "Women", 699, "👗", "Everyday kurti with a modern design.", 20),
    ("Women's Jeans", "Fashion", "Women", 999, "👖", "Versatile denim jeans.", 18),
    ("Women's Crop Top", "Fashion", "Women", 499, "👚", "Trendy crop top for casual wear.", 20),
    ("Bodycon Dress", "Fashion", "Women", 1299, "👗", "Fitted dress for parties and outings.", 12),
    ("Traditional Saree", "Fashion", "Women", 1799, "🥻", "Elegant saree for celebrations.", 12),
    ("Designer Lehenga", "Fashion", "Women", 3499, "👗", "Festive lehenga for special occasions.", 8),
    ("Anarkali Gown", "Fashion", "Women", 2499, "👗", "Flowing Anarkali gown for celebrations.", 10),

    # MOBILES
    ("Samsung Galaxy Smartphone", "Mobiles", "Samsung", 24999, "📱", "Samsung smartphone for everyday use.", 10),
    ("Vivo Smartphone", "Mobiles", "Vivo", 18999, "📱", "Vivo phone with a modern design.", 10),
    ("Oppo Smartphone", "Mobiles", "Oppo", 17999, "📱", "Oppo smartphone for daily communication.", 10),
    ("Realme Smartphone", "Mobiles", "Realme", 14999, "📱", "Realme smartphone for everyday tasks.", 12),
    ("Apple iPhone", "Mobiles", "iPhone", 59999, "📱", "Apple iPhone from the sample catalogue.", 6),
    ("Motorola Smartphone", "Mobiles", "Motorola", 16999, "📱", "Motorola smartphone with a clean design.", 10),

    # ELECTRONICS
    ("Personal Laptop", "Electronics", "Computers", 45999, "💻", "Laptop for study, work, and entertainment.", 8),
    ("Computer Monitor", "Electronics", "Displays", 9999, "🖥️", "Monitor for desktop and home-office setups.", 10),
    ("Multifunction Printer", "Electronics", "Printers", 6999, "🖨️", "Printer for everyday document printing.", 8),
    ("Digital Projector", "Electronics", "Projectors", 18999, "📽️", "Projector for presentations and home viewing.", 5),

    # ACCESSORIES
    ("Men's Wrist Watch", "Accessories", "Men", 1499, "⌚", "Classic watch for men's everyday style.", 15),
    ("Women's Wrist Watch", "Accessories", "Women", 1699, "⌚", "Elegant watch for women's everyday style.", 15),
    ("Fashion Sunglasses", "Accessories", "Eyewear", 599, "🕶️", "Sunglasses for a stylish look.", 20),
    ("Earrings Set", "Accessories", "Jewellery", 399, "💎", "Decorative earrings for different occasions.", 20),
    ("Cute Keychain", "Accessories", "Keychains", 149, "🔑", "Decorative keychain for keys and bags.", 25),
    ("Necklace Set", "Accessories", "Jewellery", 999, "📿", "Decorative necklace set for celebrations.", 12),
    ("Fashion Rings", "Accessories", "Jewellery", 299, "💍", "Fashion rings for everyday styling.", 20),

    # TOYS - 10 TYPES
    ("Teddy Bear", "Toys", "Soft Toys", 499, "🧸", "Soft cuddly teddy bear.", 20),
    ("Toy Building Blocks", "Toys", "Building Toys", 599, "🧱", "Colourful building blocks for creative play.", 15),
    ("Toy Racing Car", "Toys", "Vehicles", 299, "🏎️", "Toy racing car for imaginative play.", 20),
    ("Doll Set", "Toys", "Dolls", 699, "🪆", "Doll set for pretend-play activities.", 12),
    ("Toy Train", "Toys", "Vehicles", 799, "🚂", "Toy train for fun playtime.", 10),
    ("Puzzle Game", "Toys", "Puzzles", 349, "🧩", "Puzzle game for problem-solving practice.", 15),
    ("Toy Robot", "Toys", "Robots", 899, "🤖", "Robot toy for imaginative adventures.", 10),
    ("Football", "Toys", "Sports Toys", 449, "⚽", "Ball for recreational play.", 15),
    ("Kite", "Toys", "Outdoor Toys", 99, "🪁", "Colourful kite for outdoor fun.", 25),
    ("Toy Dinosaur", "Toys", "Figures", 399, "🦖", "Dinosaur figure for imaginative play.", 15),

    # FOOD AND HEALTH CARE
    ("Premium Almonds", "Food & Health Care", "Dry Fruits", 499, "🥜", "Almonds for snacking and cooking.", 20),
    ("Cashew Nuts", "Food & Health Care", "Dry Fruits", 549, "🥜", "Cashew nuts for snacks and recipes.", 20),
    ("Milk Chocolate", "Food & Health Care", "Chocolate", 199, "🍫", "Milk chocolate treat.", 30),
    ("Dark Chocolate", "Food & Health Care", "Chocolate", 249, "🍫", "Dark chocolate treat.", 25),

    # 8 DIFFERENT SEEDS
    ("Chia Seeds", "Food & Health Care", "Seeds", 199, "🌱", "Chia seeds for food preparation.", 20),
    ("Flax Seeds", "Food & Health Care", "Seeds", 149, "🌱", "Flax seeds for adding to meals.", 20),
    ("Pumpkin Seeds", "Food & Health Care", "Seeds", 249, "🎃", "Pumpkin seeds for snacks and toppings.", 20),
    ("Sunflower Seeds", "Food & Health Care", "Seeds", 179, "🌻", "Sunflower seeds for snacks and recipes.", 20),
    ("Sesame Seeds", "Food & Health Care", "Seeds", 129, "🌱", "Sesame seeds for cooking and baking.", 20),
    ("Watermelon Seeds", "Food & Health Care", "Seeds", 199, "🌱", "Watermelon seeds for snack mixes.", 20),
    ("Basil Seeds", "Food & Health Care", "Seeds", 159, "🌱", "Basil seeds for suitable food and drink recipes.", 20),
    ("Hemp Seeds", "Food & Health Care", "Seeds", 299, "🌱", "Hemp seeds for food preparation.", 15),
]


# ---------------- DATABASE ----------------

def connect():
    return sqlite3.connect(DB)


def init_db():
    with connect() as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL
            )
        """)

        con.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                subcategory TEXT NOT NULL,
                price REAL NOT NULL,
                emoji TEXT,
                description TEXT,
                stock INTEGER NOT NULL DEFAULT 20
            )
        """)

        con.execute("""
            CREATE TABLE IF NOT EXISTS wishlist (
                user_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                PRIMARY KEY (user_id, product_id)
            )
        """)

        con.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                customer_name TEXT NOT NULL,
                address TEXT NOT NULL,
                payment_method TEXT NOT NULL,
                payment_status TEXT NOT NULL,
                total REAL NOT NULL,
                order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        con.execute("""
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                product_name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL
            )
        """)

        count = con.execute(
            "SELECT COUNT(*) FROM products"
        ).fetchone()[0]

        if count == 0:
            con.executemany("""
                INSERT INTO products
                (name, category, subcategory, price, emoji, description, stock)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, CATALOGUE)


init_db()


# ---------------- PASSWORD HELPERS ----------------

def hash_password(password, salt=None):
    salt = salt or secrets.token_hex(16)
    hashed = hashlib.pbkdf2_hmac(
        "sha256", password.encode(),
        bytes.fromhex(salt), 200000
    ).hex()
    return hashed, salt


def verify_password(password, saved_hash, salt):
    candidate, _ = hash_password(password, salt)
    return hmac.compare_digest(candidate, saved_hash)


# ---------------- SESSION ----------------

for key, default in {
    "user_id": None,
    "username": None,
    "cart": {},
    "page": "Home",
    "last_order": None,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


def get_products():
    with connect() as con:
        return pd.read_sql_query(
            "SELECT * FROM products ORDER BY category, name", con
        )


def get_wishlist():
    with connect() as con:
        rows = con.execute(
            "SELECT product_id FROM wishlist WHERE user_id=?",
            (st.session_state.user_id,)
        ).fetchall()
    return {r[0] for r in rows}


def money(value):
    return f"₹{value:,.2f}"


def add_cart(pid, stock):
    current = st.session_state.cart.get(pid, 0)
    if current < stock:
        st.session_state.cart[pid] = current + 1
        return True
    return False


def set_page(page):
    st.session_state.page = page


# ---------------- LOGIN AND REGISTRATION ----------------

def auth_page():
    st.markdown('<div class="main-title">🛍️ ShopEase</div>',
                unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitle">Fashion, mobiles, electronics and more.</div>',
        unsafe_allow_html=True
    )
    st.divider()

    login_tab, register_tab = st.tabs(["Login", "Create Account"])

    with login_tab:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login", use_container_width=True)

        if submit:
            with connect() as con:
                user = con.execute("""
                    SELECT id, username, password_hash, salt
                    FROM users WHERE username=?
                """, (username.strip(),)).fetchone()

            if user and verify_password(password, user[2], user[3]):
                st.session_state.user_id = user[0]
                st.session_state.username = user[1]
                st.session_state.cart = {}
                st.session_state.page = "Home"
                st.rerun()
            else:
                st.error("Incorrect username or password.")

    with register_tab:
        with st.form("register_form"):
            username = st.text_input("Choose a username")
            password = st.text_input("Password (minimum 8 characters)",
                                     type="password")
            confirm = st.text_input("Confirm password", type="password")
            submit = st.form_submit_button(
                "Register", use_container_width=True
            )

        if submit:
            username = username.strip()

            if len(username) < 3:
                st.error("Username must contain at least 3 characters.")
            elif len(password) < 8:
                st.error("Password must contain at least 8 characters.")
            elif password != confirm:
                st.error("Passwords do not match.")
            else:
                hashed, salt = hash_password(password)
                try:
                    with connect() as con:
                        con.execute("""
                            INSERT INTO users (username, password_hash, salt)
                            VALUES (?, ?, ?)
                        """, (username, hashed, salt))
                    st.success("Registration successful! Please log in.")
                except sqlite3.IntegrityError:
                    st.error("This username already exists.")


# ---------------- SHARED PRODUCT CARD ----------------

def product_card(p, wishlist_ids, prefix="p"):
    pid = int(p["id"])

    with st.container(border=True):
        st.markdown(
            f"<div style='text-align:center;font-size:62px;padding:8px'>"
            f"{p['emoji']}</div>",
            unsafe_allow_html=True
        )
        st.markdown(f"**{p['name']}**")
        st.caption(f"{p['category']} · {p['subcategory']}")
        st.markdown(f"### {money(p['price'])}")
        st.caption(f"Available stock: {p['stock']}")

        with st.expander("Product details"):
            st.write(p["description"])
            st.write(f"Category: {p['category']}")
            st.write(f"Product ID: {pid}")

        if st.button("Add to Cart", key=f"{prefix}_cart_{pid}",
                     use_container_width=True):
            if add_cart(pid, int(p["stock"])):
                st.toast("Added to cart!")
                st.rerun()
            else:
                st.warning("Stock limit reached.")

        if pid in wishlist_ids:
            if st.button("♥ Remove Wishlist", key=f"{prefix}_unwish_{pid}",
                         use_container_width=True):
                with connect() as con:
                    con.execute("""
                        DELETE FROM wishlist
                        WHERE user_id=? AND product_id=?
                    """, (st.session_state.user_id, pid))
                st.rerun()
        else:
            if st.button("♡ Add to Wishlist", key=f"{prefix}_wish_{pid}",
                         use_container_width=True):
                with connect() as con:
                    con.execute("""
                        INSERT OR IGNORE INTO wishlist (user_id, product_id)
                        VALUES (?, ?)
                    """, (st.session_state.user_id, pid))
                st.toast("Added to wishlist!")
                st.rerun()


# ---------------- STORE ----------------

def store_page():
    products = get_products()
    wishlist_ids = get_wishlist()

    st.sidebar.markdown("## 🛍️ ShopEase")
    st.sidebar.caption(f"Hello, {st.session_state.username}!")

    pages = [
        "Home", "All Products", "Fashion", "Mobiles",
        "Electronics", "Accessories", "Toys",
        "Food & Health Care", "Product Details",
        "Wishlist", "Shopping Cart", "Order History",
    ]

    if st.session_state.page not in pages + ["Order Confirmation"]:
        st.session_state.page = "Home"

    page = st.sidebar.radio(
        "Navigate",
        pages,
        index=pages.index(st.session_state.page)
        if st.session_state.page in pages else 0,
        key="navigation",
    )
    st.session_state.page = page

    st.sidebar.divider()
    st.sidebar.metric("Cart items", sum(st.session_state.cart.values()))
    st.sidebar.metric("Wishlist", len(wishlist_ids))

    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state.user_id = None
        st.session_state.username = None
        st.session_state.cart = {}
        st.session_state.last_order = None
        st.session_state.page = "Home"
        st.rerun()

    # HOME
    if page == "Home":
        st.markdown('<div class="main-title">Welcome to ShopEase!</div>',
                    unsafe_allow_html=True)
        st.markdown(
            '<div class="subtitle">Everything you love, all in one place.</div>',
            unsafe_allow_html=True
        )

        a, b, c = st.columns(3)
        a.metric("Products", len(products))
        b.metric("Categories", products["category"].nunique())
        c.metric("Cart items", sum(st.session_state.cart.values()))

        st.subheader("Shop by Category")
        categories = [
            ("Fashion", "👗"),
            ("Mobiles", "📱"),
            ("Electronics", "💻"),
            ("Accessories", "⌚"),
            ("Toys", "🧸"),
            ("Food & Health Care", "🌱"),
        ]

        cols = st.columns(3)
        for i, (name, emoji) in enumerate(categories):
            with cols[i % 3]:
                with st.container(border=True):
                    st.markdown(f"<h1 style='text-align:center'>{emoji}</h1>",
                                unsafe_allow_html=True)
                    st.markdown(f"**{name}**")
                    if st.button("Explore", key=f"cat_{i}",
                                 use_container_width=True):
                        st.session_state.page = name
                        st.rerun()

        st.subheader("Popular Products")
        featured = products.head(6)
        cols = st.columns(3)
        for i, (_, p) in enumerate(featured.iterrows()):
            with cols[i % 3]:
                product_card(p, wishlist_ids, "featured")

    # ALL PRODUCTS OR CATEGORY
    elif page in [
        "All Products", "Fashion", "Mobiles", "Electronics",
        "Accessories", "Toys", "Food & Health Care"
    ]:
        st.title(f"🛍️ {page}")

        search = st.text_input(
            "🔎 Search products by name, brand, or description"
        )

        subset = products.copy()
        if page != "All Products":
            subset = subset[subset["category"] == page]

        if page == "Fashion":
            subcategories = ["All", "Men", "Women"]
            selected = st.selectbox("Shop fashion", subcategories)
            if selected != "All":
                subset = subset[subset["subcategory"] == selected]

        elif page == "Mobiles":
            brands = ["All"] + sorted(subset["subcategory"].unique().tolist())
            selected = st.selectbox("Select mobile brand", brands)
            if selected != "All":
                subset = subset[subset["subcategory"] == selected]

        elif page == "Accessories":
            kinds = ["All"] + sorted(subset["subcategory"].unique().tolist())
            selected = st.selectbox("Accessory type", kinds)
            if selected != "All":
                subset = subset[subset["subcategory"] == selected]

        elif page == "Food & Health Care":
            kinds = ["All"] + sorted(subset["subcategory"].unique().tolist())
            selected = st.selectbox("Food category", kinds)
            if selected != "All":
                subset = subset[subset["subcategory"] == selected]

        if search:
            mask = (
                subset["name"].str.contains(search, case=False, na=False)
                | subset["description"].str.contains(search, case=False, na=False)
                | subset["subcategory"].str.contains(search, case=False, na=False)
            )
            subset = subset[mask]

        st.caption(f"{len(subset)} product(s) found.")

        if subset.empty:
            st.info("No products match your search.")
        else:
            cols = st.columns(3)
            for i, (_, p) in enumerate(subset.iterrows()):
                with cols[i % 3]:
                    product_card(p, wishlist_ids, page.replace(" ", "_"))

    # DEDICATED PRODUCT DETAILS
    elif page == "Product Details":
        st.title("Product Details")
        if products.empty:
            st.info("No products available.")
        else:
            selected_name = st.selectbox(
                "Select product", products["name"].tolist()
            )
            p = products[products["name"] == selected_name].iloc[0]
            pid = int(p["id"])

            left, right = st.columns([1, 2])
            with left:
                st.markdown(
                    f"<div style='text-align:center;font-size:130px'>"
                    f"{p['emoji']}</div>",
                    unsafe_allow_html=True
                )
            with right:
                st.header(p["name"])
                st.caption(f"{p['category']} · {p['subcategory']}")
                st.subheader(money(p["price"]))
                st.write(p["description"])
                st.write(f"Stock: {p['stock']}")

                if st.button("Add to Cart", key="detail_add"):
                    if add_cart(pid, int(p["stock"])):
                        st.success("Added to cart.")
                        st.rerun()
                    else:
                        st.warning("Stock limit reached.")

                if st.button("Add to Wishlist", key="detail_wish"):
                    with connect() as con:
                        con.execute("""
                            INSERT OR IGNORE INTO wishlist
                            (user_id, product_id) VALUES (?, ?)
                        """, (st.session_state.user_id, pid))
                    st.success("Saved to wishlist.")

    # WISHLIST
    elif page == "Wishlist":
        st.title("❤️ My Wishlist")
        saved = products[products["id"].isin(wishlist_ids)]

        if saved.empty:
            st.info("Your wishlist is empty.")
        else:
            cols = st.columns(3)
            for i, (_, p) in enumerate(saved.iterrows()):
                with cols[i % 3]:
                    product_card(p, wishlist_ids, "wishlist")

    # CART AND CHECKOUT
    elif page == "Shopping Cart":
        st.title("🛒 Shopping Cart")
        cart = st.session_state.cart
        valid_items = []
        total = 0.0

        if not cart:
            st.info("Your cart is empty. Browse products to start shopping.")
        else:
            for pid in list(cart.keys()):
                found = products[products["id"] == pid]
                if found.empty:
                    continue

                p = found.iloc[0]
                qty = cart[pid]
                subtotal = float(p["price"]) * qty
                total += subtotal
                valid_items.append((pid, p, qty))

                with st.container(border=True):
                    c1, c2, c3, c4 = st.columns([3, 1, 2, 1])
                    c1.write(f"{p['emoji']} **{p['name']}**")
                    c2.write(f"Quantity: {qty}")
                    c3.write(money(subtotal))
                    if c4.button("Remove", key=f"remove_{pid}"):
                        del st.session_state.cart[pid]
                        st.rerun()

                    q1, q2, _ = st.columns([1, 1, 4])
                    if q1.button("➖", key=f"minus_{pid}"):
                        if qty <= 1:
                            del st.session_state.cart[pid]
                        else:
                            st.session_state.cart[pid] -= 1
                        st.rerun()

                    if q2.button("➕", key=f"plus_{pid}"):
                        if qty < int(p["stock"]):
                            st.session_state.cart[pid] += 1
                        else:
                            st.warning("Stock limit reached.")
                        st.rerun()

            st.divider()
            st.subheader(f"Total: {money(total)}")

            if valid_items:
                st.subheader("Checkout")
                with st.form("checkout_form"):
                    customer = st.text_input("Full name")
                    address = st.text_area("Delivery address")
                    payment = st.selectbox(
                        "Payment method",
                        ["Cash on Delivery", "UPI (Demo)", "Card (Demo)"]
                    )
                    place_order = st.form_submit_button(
                        "Place Order", use_container_width=True
                    )

                if place_order:
                    if not customer.strip() or not address.strip():
                        st.error("Enter your name and delivery address.")
                    else:
                        with connect() as con:
                            # Check current stock and save order atomically.
                            available = True
                            for pid, p, qty in valid_items:
                                row = con.execute(
                                    "SELECT stock FROM products WHERE id=?",
                                    (pid,)
                                ).fetchone()
                                if not row or row[0] < qty:
                                    available = False
                                    break

                            if not available:
                                st.error(
                                    "Some products are out of stock. "
                                    "Review your cart."
                                )
                            else:
                                status = (
                                    "Pending - Cash on Delivery"
                                    if payment == "Cash on Delivery"
                                    else "Demo only - Not charged"
                                )
                                cur = con.execute("""
                                    INSERT INTO orders
                                    (user_id, customer_name, address,
                                     payment_method, payment_status, total)
                                    VALUES (?, ?, ?, ?, ?, ?)
                                """, (
                                    st.session_state.user_id,
                                    customer.strip(), address.strip(),
                                    payment, status, total
                                ))
                                order_id = cur.lastrowid

                                for pid, p, qty in valid_items:
                                    con.execute("""
                                        INSERT INTO order_items
                                        (order_id, product_id, product_name,
                                         quantity, price)
                                        VALUES (?, ?, ?, ?, ?)
                                    """, (
                                        order_id, pid, p["name"], qty,
                                        float(p["price"])
                                    ))
                                    con.execute("""
                                        UPDATE products SET stock = stock - ?
                                        WHERE id = ?
                                    """, (qty, pid))

                                st.session_state.cart = {}
                                st.session_state.last_order = order_id
                                st.session_state.page = "Order Confirmation"
                                st.rerun()

    # ORDER HISTORY
    elif page == "Order History":
        st.title("📦 My Order History")
        with connect() as con:
            orders = pd.read_sql_query("""
                SELECT id AS order_id, order_date, total,
                       payment_method, payment_status
                FROM orders WHERE user_id = ?
                ORDER BY id DESC
            """, con, params=(st.session_state.user_id,))

        if orders.empty:
            st.info("You haven't placed any orders yet.")
        else:
            st.dataframe(orders, use_container_width=True, hide_index=True)
            order_id = st.selectbox("Select an order", orders["order_id"].tolist())

            with connect() as con:
                details = pd.read_sql_query("""
                    SELECT product_name, quantity, price
                    FROM order_items WHERE order_id = ?
                """, con, params=(int(order_id),))

            st.subheader(f"Order #{order_id}")
            st.dataframe(details, use_container_width=True, hide_index=True)


# ---------------- ORDER CONFIRMATION ----------------

def confirmation_page():
    order_id = st.session_state.last_order

    st.title("✅ Order Confirmation")
    if not order_id:
        st.info("No recent order to show.")
        if st.button("Continue Shopping"):
            st.session_state.page = "Home"
            st.rerun()
        return

    with connect() as con:
        order = con.execute("""
            SELECT customer_name, address, payment_method,
                   payment_status, total, order_date
            FROM orders WHERE id = ? AND user_id = ?
        """, (order_id, st.session_state.user_id)).fetchone()

        items = pd.read_sql_query("""
            SELECT product_name, quantity, price
            FROM order_items WHERE order_id = ?
        """, con, params=(order_id,))

    if not order:
        st.error("Order not found.")
        return

    st.success("Your order has been placed!")
    st.subheader(f"Order ID: #{order_id}")
    st.write(f"**Customer:** {order[0]}")
    st.write(f"**Delivery address:** {order[1]}")
    st.write(f"**Payment method:** {order[2]}")
    st.write(f"**Payment status:** {order[3]}")
    st.write(f"**Date:** {order[5]}")
    st.dataframe(items, use_container_width=True, hide_index=True)
    st.subheader(f"Total: {money(order[4])}")

    if order[2] != "Cash on Delivery":
        st.warning(
            "This is a demo payment selection. No real payment was made."
        )

    if st.button("Continue Shopping", use_container_width=True):
        st.session_state.last_order = None
        st.session_state.page = "Home"
        st.rerun()


# ---------------- MAIN APP ----------------

if st.session_state.user_id is None:
    auth_page()
elif st.session_state.page == "Order Confirmation":
    confirmation_page()
else:
    store_page()
