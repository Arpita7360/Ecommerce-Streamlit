
import sqlite3
import hashlib
import hmac
import secrets
import streamlit as st
import pandas as pd

DB = "shopease.db"

st.set_page_config(
    page_title="SHOP EASE | Online Store",
    page_icon="🛍️",
    layout="wide"
)

# ---------------- BLACK & WHITE DESIGN ----------------

st.markdown("""
<style>
.stApp {
    background-color: #080808;
    color: #ffffff;
}
[data-testid="stHeader"] {
    background-color: #080808;
}
[data-testid="stSidebar"] {
    background-color: #111111;
}
h1, h2, h3, h4, p, label, span, li {
    color: #ffffff;
}
div[data-testid="stMarkdownContainer"] p {
    color: #eeeeee;
}
.stButton button, .stFormSubmitButton button {
    background: #ffffff;
    color: #080808;
    border: 1px solid #ffffff;
    border-radius: 8px;
    font-weight: 600;
    min-height: 40px;
}
.stButton button:hover, .stFormSubmitButton button:hover {
    background: #d8d8d8;
    color: #000000;
    border: 1px solid #d8d8d8;
}
input, textarea {
    color: #ffffff !important;
}
[data-baseweb="input"], [data-baseweb="textarea"] {
    background: #171717;
}
[data-baseweb="select"] > div {
    background: #171717;
}
.product-card {
    border: 1px solid #3a3a3a;
    padding: 14px;
    border-radius: 12px;
    background: #111111;
}
.hero {
    padding: 30px 10px;
    background: #141414;
    border: 1px solid #333333;
    border-radius: 15px;
    margin-bottom: 20px;
}
.hero p {
    color: #cccccc;
}
hr {
    border-color: #333333;
}
</style>
""", unsafe_allow_html=True)


# ---------------- PRODUCT CATALOGUE ----------------
# Prices are sample prices in INR.
# Photos are external Unsplash image URLs.

def photo(photo_id):
    return (
        f"https://images.unsplash.com/{photo_id}"
        "?auto=format&fit=crop&w=800&q=80"
    )


PRODUCTS = [
    # MEN'S FASHION
    ("Men's Shirt", "Fashion", "Men", 899, "👔",
     "Classic men's casual shirt.", "photo-1598033129183-c4f50c736f10"),
    ("Men's T-Shirt", "Fashion", "Men", 499, "👕",
     "Comfortable everyday T-shirt.", "photo-1521572163474-6864f9cf17ab"),
    ("Men's Jeans", "Fashion", "Men", 1199, "👖",
     "Everyday denim jeans.", "photo-1542272604-787c3835535d"),
    ("Men's Jacket", "Fashion", "Men", 1799, "🧥",
     "Stylish jacket for cool weather.", "photo-1551028719-00167b16eac5"),
    ("Men's Kurta", "Fashion", "Men", 999, "🥻",
     "Traditional Indian kurta.", "photo-1610030469983-98e550d6193c"),
    ("Men's Blazer", "Fashion", "Men", 2499, "🤵",
     "Formal blazer for special occasions.", "photo-1591047139829-d91aecb6caea"),

    # WOMEN'S FASHION
    ("Women's Kurti", "Fashion", "Women", 799, "👗",
     "Everyday ethnic kurti.", "photo-1583391733956-6c78276477e3"),
    ("Women's Jeans", "Fashion", "Women", 1199, "👖",
     "Modern fit denim jeans.", "photo-1541099649105-f69ad21f3246"),
    ("Women's Crop Top", "Fashion", "Women", 599, "👚",
     "Trendy crop top.", "photo-1551163943-3f6a855d1153"),
    ("Bodycon Dress", "Fashion", "Women", 1499, "👗",
     "Elegant fitted dress.", "photo-1595777457583-95e059d581b8"),
    ("Women's Saree", "Fashion", "Women", 1999, "🥻",
     "Traditional saree for celebrations.", "photo-1610030469983-98e550d6193c"),
    ("Lehenga", "Fashion", "Women", 3499, "👗",
     "Festive lehenga design.", "photo-1583391733956-6c78276477e3"),
    ("Anarkali Gown", "Fashion", "Women", 2799, "👗",
     "Flowing Anarkali-style gown.", "photo-1595777457583-95e059d581b8"),

    # MOBILES
    ("Samsung Smartphone", "Mobiles", "Samsung", 18999, "📱",
     "Samsung smartphone. Model and specifications vary.", "photo-1511707171634-5f897ff02aa9"),
    ("Vivo Smartphone", "Mobiles", "Vivo", 15999, "📱",
     "Vivo smartphone. Model and specifications vary.", "photo-1511707171634-5f897ff02aa9"),
    ("Oppo Smartphone", "Mobiles", "Oppo", 16999, "📱",
     "Oppo smartphone. Model and specifications vary.", "photo-1511707171634-5f897ff02aa9"),
    ("Realme Smartphone", "Mobiles", "Realme", 13999, "📱",
     "Realme smartphone. Model and specifications vary.", "photo-1511707171634-5f897ff02aa9"),
    ("iPhone", "Mobiles", "Apple", 59999, "📱",
     "Apple iPhone. Model and specifications vary.", "photo-1592750475338-74b7b21085ab"),
    ("Motorola Smartphone", "Mobiles", "Motorola", 14999, "📱",
     "Motorola smartphone. Model and specifications vary.", "photo-1511707171634-5f897ff02aa9"),

    # ELECTRONICS
    ("Laptop", "Electronics", "Computers", 45999, "💻",
     "Laptop for study and everyday work.", "photo-1498050108023-c5249f4df085"),
    ("Monitor", "Electronics", "Computers", 12999, "🖥️",
     "Computer monitor for work and entertainment.", "photo-1527443224154-c4a3942d3acf"),
    ("Printer", "Electronics", "Office", 6999, "🖨️",
     "Printer for home or office.", "photo-1612815154858-60aa4c59eaa6"),
    ("Projector", "Electronics", "Office", 18999, "📽️",
     "Projector for presentations and entertainment.", "photo-1528395874238-34ebe249b3f2"),

    # ACCESSORIES
    ("Men's Watch", "Accessories", "Men", 1499, "⌚",
     "Classic men's wristwatch.", "photo-1523275335684-37898b6baf30"),
    ("Women's Watch", "Accessories", "Women", 1799, "⌚",
     "Elegant women's wristwatch.", "photo-1524592094714-0f0654e20314"),
    ("Sunglasses", "Accessories", "Unisex", 699, "🕶️",
     "Stylish sunglasses.", "photo-1511499767150-a48a237f0083"),
    ("Earrings", "Accessories", "Women", 399, "💎",
     "Decorative earrings.", "photo-1535632066927-ab7c9ab60908"),
    ("Keychain", "Accessories", "Unisex", 149, "🔑",
     "Decorative everyday keychain.", "photo-1582562124811-c09040d0a901"),
    ("Necklace Set", "Accessories", "Women", 999, "📿",
     "Necklace set for celebrations.", "photo-1611652022419-a9419f74343d"),
    ("Rings", "Accessories", "Unisex", 499, "💍",
     "Decorative rings.", "photo-1605100804763-247f67b3557e"),

    # TEN DIFFERENT TOYS
    ("Teddy Bear", "Toys", "Soft Toys", 499, "🧸",
     "Soft cuddly teddy bear.", "photo-1559454403-b8fb88521f11"),
    ("Toy Car", "Toys", "Vehicles", 299, "🚗",
     "Toy car for imaginative play.", "photo-1594787318286-3d835c1d207f"),
    ("Building Blocks", "Toys", "Learning Toys", 699, "🧱",
     "Creative construction building blocks.", "photo-1587654780291-39c9404d746b"),
    ("Toy Train", "Toys", "Vehicles", 599, "🚂",
     "Toy train set.", "photo-1516627145497-ae6968895b74"),
    ("Doll", "Toys", "Dolls", 499, "🪆",
     "Doll for pretend play.", "photo-1599623560574-39d485900c95"),
    ("Puzzle Game", "Toys", "Learning Toys", 349, "🧩",
     "Puzzle to encourage problem-solving.", "photo-1606092195730-5d7b9af1efc5"),
    ("Remote Control Car", "Toys", "Vehicles", 1299, "🏎️",
     "Remote-controlled toy car.", "photo-1594787318286-3d835c1d207f"),
    ("Toy Robot", "Toys", "Robots", 899, "🤖",
     "Robot toy for play and collecting.", "photo-1535378620166-273708d44e4c"),
    ("Toy Dinosaur", "Toys", "Animals", 399, "🦖",
     "Dinosaur figure for imaginative play.", "photo-1511497584788-876760111969"),
    ("Art and Craft Kit", "Toys", "Creative Toys", 449, "🎨",
     "Creative art and craft kit.", "photo-1513364776144-60967b0f800f"),

    # FOOD AND HEALTHCARE
    ("Mixed Dry Fruits", "Food & Healthcare", "Dry Fruits", 699, "🥜",
     "Assorted dry fruits for snacking.", "photo-1608797178974-15b35a64ede9"),
    ("Chocolate Box", "Food & Healthcare", "Chocolate", 499, "🍫",
     "Assorted chocolate gift box.", "photo-1548907040-4d42c8e2e6c9"),

    # EIGHT TYPES OF SEEDS
    ("Chia Seeds", "Food & Healthcare", "Seeds", 199, "🌱",
     "Chia seeds for food preparation.", "photo-1515543904379-3d757afe72e4"),
    ("Flax Seeds", "Food & Healthcare", "Seeds", 149, "🌱",
     "Flax seeds for everyday recipes.", "photo-1515543904379-3d757afe72e4"),
    ("Pumpkin Seeds", "Food & Healthcare", "Seeds", 249, "🌱",
     "Pumpkin seeds for snacks and salads.", "photo-1574570173589-0a4e5aab3c2c"),
    ("Sunflower Seeds", "Food & Healthcare", "Seeds", 179, "🌱",
     "Sunflower seeds for snacks.", "photo-1501436513145-30f24e19fcc4"),
    ("Sesame Seeds", "Food & Healthcare", "Seeds", 129, "🌱",
     "Sesame seeds for cooking.", "photo-1515543904379-3d757afe72e4"),
    ("Watermelon Seeds", "Food & Healthcare", "Seeds", 199, "🌱",
     "Watermelon seeds for snacking.", "photo-1515543904379-3d757afe72e4"),
    ("Basil Seeds", "Food & Healthcare", "Seeds", 149, "🌱",
     "Basil seeds for drinks and recipes.", "photo-1515543904379-3d757afe72e4"),
    ("Hemp Seeds", "Food & Healthcare", "Seeds", 299, "🌱",
     "Hemp seeds for food preparation.", "photo-1515543904379-3d757afe72e4"),
]


# ---------------- DATABASE ----------------

def db():
    return sqlite3.connect(DB)


def init_db():
    with db() as con:
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
                name TEXT UNIQUE NOT NULL,
                category TEXT NOT NULL,
                subcategory TEXT,
                price REAL NOT NULL,
                emoji TEXT,
                description TEXT,
                image_url TEXT,
                stock INTEGER NOT NULL DEFAULT 15
            )
        """)
        con.execute("""
            CREATE TABLE IF NOT EXISTS wishlist (
                user_id INTEGER,
                product_id INTEGER,
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

        # Insert each catalogue item once.
        for name, category, subcategory, price, emoji, desc, img in PRODUCTS:
            con.execute("""
                INSERT OR IGNORE INTO products
                (name, category, subcategory, price, emoji,
                 description, image_url, stock)
                VALUES (?, ?, ?, ?, ?, ?, ?, 15)
            """, (
                name, category, subcategory, price, emoji,
                desc, photo(img)
            ))


init_db()


# ---------------- ACCOUNT HELPERS ----------------

def password_hash(password, salt):
    return hashlib.pbkdf2_hmac(
        "sha256", password.encode(),
        bytes.fromhex(salt), 200000
    ).hex()


def money(value):
    return f"₹{value:,.2f}"


def get_products():
    with db() as con:
        return pd.read_sql_query(
            "SELECT * FROM products ORDER BY category, name", con
        )


def wishlist_ids():
    with db() as con:
        rows = con.execute(
            "SELECT product_id FROM wishlist WHERE user_id = ?",
            (st.session_state.user_id,)
        ).fetchall()
    return {r[0] for r in rows}


def toggle_wishlist(pid):
    with db() as con:
        found = con.execute("""
            SELECT 1 FROM wishlist
            WHERE user_id = ? AND product_id = ?
        """, (st.session_state.user_id, pid)).fetchone()

        if found:
            con.execute("""
                DELETE FROM wishlist
                WHERE user_id = ? AND product_id = ?
            """, (st.session_state.user_id, pid))
        else:
            con.execute("""
                INSERT OR IGNORE INTO wishlist (user_id, product_id)
                VALUES (?, ?)
            """, (st.session_state.user_id, pid))


def add_cart(pid, stock):
    current = st.session_state.cart.get(pid, 0)
    if current < stock:
        st.session_state.cart[pid] = current + 1
        return True
    return False


# ---------------- SESSION STATE ----------------

for key, default in {
    "user_id": None,
    "username": None,
    "cart": {},
    "page": "Home",
    "selected_product": None,
    "last_order": None,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


# ---------------- LOGIN AND REGISTER ----------------

def auth_page():
    st.markdown("""
    <div class="hero">
      <h1>SHOP EASE</h1>
      <h3>Your style. Your technology. Your store.</h3>
      <p>Discover fashion, mobiles, electronics, toys and everyday essentials.</p>
    </div>
    """, unsafe_allow_html=True)

    login_tab, register_tab = st.tabs(["Login", "Create Account"])

    with login_tab:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login", use_container_width=True)

        if submit:
            with db() as con:
                row = con.execute("""
                    SELECT id, username, password_hash, salt
                    FROM users WHERE username = ?
                """, (username.strip(),)).fetchone()

            if row and hmac.compare_digest(
                password_hash(password, row[3]), row[2]
            ):
                st.session_state.user_id = row[0]
                st.session_state.username = row[1]
                st.session_state.cart = {}
                st.session_state.page = "Home"
                st.rerun()
            else:
                st.error("Incorrect username or password.")

    with register_tab:
        with st.form("register_form"):
            username = st.text_input("Create username")
            password = st.text_input("Create password", type="password")
            confirm = st.text_input("Confirm password", type="password")
            submit = st.form_submit_button(
                "Register", use_container_width=True
            )

        if submit:
            username = username.strip()

            if len(username) < 3:
                st.error("Username must have at least 3 characters.")
            elif len(password) < 8:
                st.error("Use a password of at least 8 characters.")
            elif password != confirm:
                st.error("Passwords do not match.")
            else:
                salt = secrets.token_hex(16)
                hashed = password_hash(password, salt)
                try:
                    with db() as con:
                        con.execute("""
                            INSERT INTO users (username, password_hash, salt)
                            VALUES (?, ?, ?)
                        """, (username, hashed, salt))
                    st.success("Account created. Please log in.")
                except sqlite3.IntegrityError:
                    st.error("This username is already registered.")


# ---------------- PRODUCT CARD ----------------

def product_card(p, prefix="product"):
    pid = int(p["id"])

    st.markdown('<div class="product-card">', unsafe_allow_html=True)
    st.image(p["image_url"], use_container_width=True)
    st.markdown(f"**{p['name']}**")
    st.caption(f"{p['category']} · {p['subcategory']}")
    st.markdown(f"### {money(p['price'])}")
    st.caption(f"Available stock: {p['stock']}")
    st.markdown('</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    if c1.button("View Details", key=f"{prefix}_details_{pid}",
                 use_container_width=True):
        st.session_state.selected_product = pid
        st.session_state.page = "Product Details"
        st.rerun()

    if c2.button("♡ Wishlist", key=f"{prefix}_wish_{pid}",
                 use_container_width=True):
        toggle_wishlist(pid)
        st.toast("Wishlist updated.")
        st.rerun()

    if st.button("Add to Cart", key=f"{prefix}_cart_{pid}",
                 use_container_width=True):
        if add_cart(pid, int(p["stock"])):
            st.toast("Added to cart.")
            st.rerun()
        else:
            st.warning("Stock limit reached.")


# ---------------- STORE PAGES ----------------

def store_page():
    products = get_products()
    wish = wishlist_ids()

    with st.sidebar:
        st.markdown("# SHOP EASE")
        st.caption(f"Hello, {st.session_state.username}!")
        st.divider()

        pages = [
            "Home", "Fashion", "Mobiles", "Electronics",
            "Accessories", "Toys", "Food & Healthcare",
            "Search All Products", "Product Details",
            "Shopping Cart", "Wishlist", "Order History",
            "Order Confirmation"
        ]

        current_page = st.session_state.page
        if current_page not in pages:
            current_page = "Home"

        selected_page = st.radio(
            "MENU", pages,
            index=pages.index(current_page)
        )
        st.session_state.page = selected_page

        st.divider()
        st.metric("Cart Items", sum(st.session_state.cart.values()))
        st.metric("Wishlist", len(wish))

        if st.button("Logout", use_container_width=True):
            st.session_state.user_id = None
            st.session_state.username = None
            st.session_state.cart = {}
            st.session_state.last_order = None
            st.session_state.page = "Home"
            st.rerun()

    page = st.session_state.page

    if page == "Order Confirmation":
        confirmation_page()
        return

    if page == "Home":
        st.markdown("""
        <div class="hero">
          <h1>SHOP EASE</h1>
          <h2>Find your style. Discover your favourites.</h2>
          <p>Fashion, mobiles, electronics, accessories, toys and more.</p>
        </div>
        """, unsafe_allow_html=True)

        a, b, c = st.columns(3)
        a.metric("Products", len(products))
        b.metric("Categories", products["category"].nunique())
        c.metric("Saved Favourites", len(wish))

        st.subheader("Explore Categories")
        categories = [
            ("Fashion", "Explore men's and women's styles"),
            ("Mobiles", "Explore popular mobile brands"),
            ("Electronics", "Computers and office electronics"),
            ("Accessories", "Watches, jewellery and more"),
            ("Toys", "Fun toys for different interests"),
            ("Food & Healthcare", "Dry fruits, chocolate and seeds"),
        ]

        cols = st.columns(3)
        for i, (cat, desc) in enumerate(categories):
            with cols[i % 3]:
                with st.container(border=True):
                    st.subheader(cat)
                    st.caption(desc)
                    if st.button("Explore", key=f"category_{i}",
                                 use_container_width=True):
                        st.session_state.page = cat
                        st.rerun()

        st.subheader("Popular Products")
        cols = st.columns(4)
        for i, (_, p) in enumerate(products.head(4).iterrows()):
            with cols[i]:
                product_card(p, "home")

    elif page in [
        "Fashion", "Mobiles", "Electronics", "Accessories",
        "Toys", "Food & Healthcare"
    ]:
        st.title(page)
        subset = products[products["category"] == page].copy()

        if page == "Fashion":
            gender = st.selectbox(
                "Shop by section",
                ["All Fashion", "Men", "Women"]
            )
            if gender != "All Fashion":
                subset = subset[subset["subcategory"] == gender]

        elif page == "Mobiles":
            brand = st.selectbox(
                "Choose mobile brand",
                ["All Brands"] + sorted(subset["subcategory"].unique())
            )
            if brand != "All Brands":
                subset = subset[subset["subcategory"] == brand]

        elif page == "Accessories":
            group = st.selectbox(
                "Choose accessories",
                ["All Accessories"] + sorted(subset["subcategory"].unique())
            )
            if group != "All Accessories":
                subset = subset[subset["subcategory"] == group]

        elif page == "Food & Healthcare":
            group = st.selectbox(
                "Choose product type",
                ["All Products"] + sorted(subset["subcategory"].unique())
            )
            if group != "All Products":
                subset = subset[subset["subcategory"] == group]

        cols = st.columns(3)
        for i, (_, p) in enumerate(subset.iterrows()):
            with cols[i % 3]:
                product_card(p, page.replace(" ", "_"))

    elif page == "Search All Products":
        st.title("Search Products")
        query = st.text_input("Search by product name or brand")
        categories = ["All"] + sorted(products["category"].unique())
        category = st.selectbox("Category", categories)

        subset = products.copy()
        if query:
            mask = (
                subset["name"].str.contains(query, case=False, na=False)
                | subset["subcategory"].str.contains(
                    query, case=False, na=False
                )
            )
            subset = subset[mask]

        if category != "All":
            subset = subset[subset["category"] == category]

        st.caption(f"{len(subset)} result(s)")
        if subset.empty:
            st.info("No products found.")
        else:
            cols = st.columns(3)
            for i, (_, p) in enumerate(subset.iterrows()):
                with cols[i % 3]:
                    product_card(p, "search")

    elif page == "Product Details":
        st.title("Product Details")

        if products.empty:
            st.info("No products available.")
        else:
            ids = products["id"].tolist()
            default_id = st.session_state.selected_product
            if default_id not in ids:
                default_id = ids[0]

            p = products[products["id"] == default_id].iloc[0]
            pid = int(p["id"])

            left, right = st.columns([1, 1])
            with left:
                st.image(p["image_url"], use_container_width=True)
            with right:
                st.title(p["name"])
                st.caption(f"{p['category']} · {p['subcategory']}")
                st.header(money(p["price"]))
                st.write(p["description"])
                st.write(f"**Stock available:** {p['stock']}")

                if st.button("Add to Cart", use_container_width=True):
                    if add_cart(pid, int(p["stock"])):
                        st.success("Added to cart.")
                        st.rerun()
                    else:
                        st.warning("Stock limit reached.")

                if st.button("♡ Add to Wishlist", use_container_width=True):
                    toggle_wishlist(pid)
                    st.toast("Wishlist updated.")
                    st.rerun()

            st.divider()
            st.subheader("Choose another product")
            chosen = st.selectbox(
                "Product", products["name"].tolist(),
                index=products.index[products["id"] == pid][0]
            )
            if chosen != p["name"]:
                st.session_state.selected_product = int(
                    products.loc[products["name"] == chosen, "id"].iloc[0]
                )
                st.rerun()

    elif page == "Shopping Cart":
        st.title("🛒 Shopping Cart")
        cart = st.session_state.cart
        total = 0.0
        rows = []

        for pid, qty in list(cart.items()):
            found = products[products["id"] == pid]
            if found.empty:
                continue
            p = found.iloc[0]
            subtotal = float(p["price"]) * qty
            total += subtotal
            rows.append((pid, p, qty, subtotal))

        if not rows:
            st.info("Your cart is empty. Browse products to get started.")
        else:
            for pid, p, qty, subtotal in rows:
                with st.container(border=True):
                    image_col, info_col, action_col = st.columns([1, 3, 2])
                    with image_col:
                        st.image(p["image_url"], use_container_width=True)
                    with info_col:
                        st.subheader(p["name"])
                        st.write(money(p["price"]))
                        st.write(f"Quantity: {qty}")
                        st.write(f"Subtotal: {money(subtotal)}")
                    with action_col:
                        if st.button("➖ Decrease", key=f"minus_{pid}"):
                            if qty <= 1:
                                del st.session_state.cart[pid]
                            else:
                                st.session_state.cart[pid] -= 1
                            st.rerun()

                        if st.button("➕ Increase", key=f"plus_{pid}"):
                            if qty < int(p["stock"]):
                                st.session_state.cart[pid] += 1
                                st.rerun()
                            else:
                                st.warning("Stock limit reached.")

                        if st.button("Remove Item", key=f"remove_{pid}"):
                            del st.session_state.cart[pid]
                            st.rerun()

            st.divider()
            st.header(f"Total: {money(total)}")
            st.subheader("Checkout")

            with st.form("checkout_form"):
                customer_name = st.text_input("Full name")
                address = st.text_area("Delivery address")
                payment = st.selectbox(
                    "Payment method",
                    ["Cash on Delivery", "UPI (Demo)", "Card (Demo)"]
                )
                submit = st.form_submit_button(
                    "Place Order", use_container_width=True
                )

            if submit:
                if not customer_name.strip() or not address.strip():
                    st.error("Please enter your name and delivery address.")
                else:
                    with db() as con:
                        # Validate all stock before saving the order.
                        valid = True
                        for pid, p, qty, subtotal in rows:
                            stock = con.execute(
                                "SELECT stock FROM products WHERE id = ?",
                                (pid,)
                            ).fetchone()
                            if not stock or stock[0] < qty:
                                valid = False
                                break

                        if not valid:
                            st.error("Insufficient stock. Refresh your cart.")
                        else:
                            status = (
                                "Pending - Cash on Delivery"
                                if payment == "Cash on Delivery"
                                else "Demo only - Not charged"
                            )
                            cursor = con.execute("""
                                INSERT INTO orders
                                (user_id, customer_name, address,
                                 payment_method, payment_status, total)
                                VALUES (?, ?, ?, ?, ?, ?)
                            """, (
                                st.session_state.user_id,
                                customer_name.strip(), address.strip(),
                                payment, status, total
                            ))
                            order_id = cursor.lastrowid

                            for pid, p, qty, subtotal in rows:
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
                                    UPDATE products
                                    SET stock = stock - ?
                                    WHERE id = ?
                                """, (qty, pid))

                            st.session_state.cart = {}
                            st.session_state.last_order = order_id
                            st.session_state.page = "Order Confirmation"
                            st.rerun()

    elif page == "Wishlist":
        st.title("♡ My Wishlist")
        saved = products[products["id"].isin(wish)]

        if saved.empty:
            st.info("Your wishlist is empty.")
        else:
            cols = st.columns(3)
            for i, (_, p) in enumerate(saved.iterrows()):
                with cols[i % 3]:
                    product_card(p, "wishlist")
                    if st.button(
                        "Remove from Wishlist",
                        key=f"wish_remove_{p['id']}",
                        use_container_width=True
                    ):
                        toggle_wishlist(int(p["id"]))
                        st.rerun()

    elif page == "Order History":
        st.title("📦 My Order History")
        with db() as con:
            orders = pd.read_sql_query("""
                SELECT id AS order_id, order_date, total,
                       payment_method, payment_status
                FROM orders
                WHERE user_id = ?
                ORDER BY id DESC
            """, con, params=(st.session_state.user_id,))

        if orders.empty:
            st.info("You have not placed any orders yet.")
        else:
            st.dataframe(orders, use_container_width=True, hide_index=True)
            order_id = st.selectbox(
                "Select an order",
                orders["order_id"].tolist()
            )
            with db() as con:
                items = pd.read_sql_query("""
                    SELECT product_name, quantity, price
                    FROM order_items WHERE order_id = ?
                """, con, params=(int(order_id),))
            st.subheader(f"Order #{order_id}")
            st.dataframe(items, use_container_width=True, hide_index=True)


# ---------------- ORDER CONFIRMATION ----------------

def confirmation_page():
    st.title("✅ Order Confirmed")
    order_id = st.session_state.last_order

    if not order_id:
        st.info("No recent order is selected.")
        if st.button("Continue Shopping"):
            st.session_state.page = "Home"
            st.rerun()
        return

    with db() as con:
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

    st.success("Thank you! Your order has been recorded.")
    st.subheader(f"Order ID: #{order_id}")
    st.write(f"**Customer:** {order[0]}")
    st.write(f"**Delivery address:** {order[1]}")
    st.write(f"**Payment method:** {order[2]}")
    st.write(f"**Payment status:** {order[3]}")
    st.write(f"**Order date:** {order[5]}")
    st.subheader("Order Items")
    st.dataframe(items, use_container_width=True, hide_index=True)
    st.header(f"Total: {money(order[4])}")

    st.warning(
        "Demo payment only: this website does not charge a real card or UPI account."
    )

    if st.button("Continue Shopping", use_container_width=True):
        st.session_state.last_order = None
        st.session_state.page = "Home"
        st.rerun()


# ---------------- RUN APP ----------------

if st.session_state.user_id is None:
    auth_page()
else:
    store_page()
