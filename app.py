import streamlit as st
import pandas as pd
from urllib.parse import quote

st.set_page_config(
    page_title="ShopNova | Online Shopping",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- COLOURFUL DARK THEME ----------
st.markdown("""
<style>
:root { color-scheme: dark; }
.stApp {
    background: radial-gradient(circle at top left, #202047 0, #101018 38%, #08080d 100%);
    color: #ffffff;
}
[data-testid="stHeader"] { background: rgba(0,0,0,0); }
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #17172b 0%, #0d0d15 100%);
    border-right: 1px solid #343454;
}
h1, h2, h3, h4, p, label, span, div { color: inherit; }
.hero {
    padding: 28px 30px;
    border-radius: 22px;
    background: linear-gradient(115deg, #6d28d9, #db2777 52%, #f97316);
    color: white;
    margin-bottom: 20px;
    box-shadow: 0 12px 35px rgba(219,39,119,.20);
}
.hero h1 { color: white; font-size: 2.35rem; margin-bottom: 6px; }
.hero p { color: white; font-size: 1.05rem; margin: 0; }
.product-card {
    background: linear-gradient(180deg, #20202d, #15151f);
    border: 1px solid #343445;
    border-radius: 17px;
    padding: 12px;
    margin-bottom: 18px;
    min-height: 100px;
}
.product-name { font-weight: 700; font-size: 1rem; color: #fff; margin: 8px 0 3px; }
.product-category { color: #b9b9d2; font-size: .82rem; }
.price { color: #6ee7b7; font-size: 1.1rem; font-weight: 800; }
.pill {
    display: inline-block; padding: 5px 10px; border-radius: 999px;
    background: #29294b; color: #ddd6fe; font-size: .78rem; margin: 3px 4px 3px 0;
}
div.stButton > button {
    background: linear-gradient(90deg, #7c3aed, #db2777);
    color: white; border: 0; border-radius: 10px; font-weight: 700;
    min-height: 40px;
}
div.stButton > button:hover { border: 1px solid #f9a8d4; color: white; }
div[data-testid="stTextInput"] input, div[data-testid="stNumberInput"] input,
div[data-testid="stSelectbox"] div[data-baseweb="select"],
div[data-testid="stTextArea"] textarea {
    background: #20202d !important; color: #fff !important;
}
[data-testid="stExpander"] {
    background: #171721; border: 1px solid #343445; border-radius: 12px;
}
hr { border-color: #38384c; }
.small-note { color: #b8b8cb; font-size: .85rem; }
</style>
""", unsafe_allow_html=True)

# ---------- PRODUCT CATALOG ----------
# Images are hosted online. Replace any image URL with a local image path if desired.
PHOTO = {
    "shirt": "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?auto=format&fit=crop&w=800&q=85",
    "tshirt": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?auto=format&fit=crop&w=800&q=85",
    "jeans": "https://images.unsplash.com/photo-1542272604-787c3835535d?auto=format&fit=crop&w=800&q=85",
    "jacket": "https://images.unsplash.com/photo-1551028719-00167b16eac5?auto=format&fit=crop&w=800&q=85",
    "kurta": "https://images.unsplash.com/photo-1610030469983-98e550d6193c?auto=format&fit=crop&w=800&q=85",
    "blazer": "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?auto=format&fit=crop&w=800&q=85",
    "dress": "https://images.unsplash.com/photo-1595777457583-95e059d581b8?auto=format&fit=crop&w=800&q=85",
    "saree": "https://images.unsplash.com/photo-1610030469983-98e550d6193c?auto=format&fit=crop&w=800&q=85",
    "crop": "https://images.unsplash.com/photo-1509631179647-0177331693ae?auto=format&fit=crop&w=800&q=85",
    "lehenga": "https://images.unsplash.com/photo-1583391733956-6c78276477e8?auto=format&fit=crop&w=800&q=85",
    "phone": "https://images.unsplash.com/photo-1598327105666-5b89351aff97?auto=format&fit=crop&w=800&q=85",
    "iphone": "https://images.unsplash.com/photo-1592750475338-74b7b21085ab?auto=format&fit=crop&w=800&q=85",
    "laptop": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&w=800&q=85",
    "monitor": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?auto=format&fit=crop&w=800&q=85",
    "printer": "https://images.unsplash.com/photo-1612815154858-60aa4c59eaa6?auto=format&fit=crop&w=800&q=85",
    "projector": "https://images.unsplash.com/photo-1585647347483-22b66260dfff?auto=format&fit=crop&w=800&q=85",
    "watch": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=800&q=85",
    "sunglasses": "https://images.unsplash.com/photo-1511499767150-a48a237f0083?auto=format&fit=crop&w=800&q=85",
    "earrings": "https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?auto=format&fit=crop&w=800&q=85",
    "necklace": "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?auto=format&fit=crop&w=800&q=85",
    "ring": "https://images.unsplash.com/photo-1605100804763-247f67b3557e?auto=format&fit=crop&w=800&q=85",
    "keychain": "https://images.unsplash.com/photo-1617038220319-276d3cfab638?auto=format&fit=crop&w=800&q=85",
    "toy": "https://images.unsplash.com/photo-1566576912321-d58ddd7a6088?auto=format&fit=crop&w=800&q=85",
    "teddy": "https://images.unsplash.com/photo-1559454403-b8fb88521f11?auto=format&fit=crop&w=800&q=85",
    "puzzle": "https://images.unsplash.com/photo-1606503153255-59d8b8b821b5?auto=format&fit=crop&w=800&q=85",
    "food": "https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=800&q=85",
    "chocolate": "https://images.unsplash.com/photo-1548907040-4d42a7f5e5f8?auto=format&fit=crop&w=800&q=85",
    "nuts": "https://images.unsplash.com/photo-1508061253366-f7da158b6d46?auto=format&fit=crop&w=800&q=85",
    "seeds": "https://images.unsplash.com/photo-1518843875459-f738682238a6?auto=format&fit=crop&w=800&q=85",
}

items = []
def add(category, subcategory, name, price, image, description):
    items.append({
        "id": len(items) + 1, "category": category, "subcategory": subcategory,
        "name": name, "price": int(price), "image": PHOTO[image],
        "description": description
    })

# Fashion - men
for sub, name, price, img, desc in [
    ("Men", "Classic Formal Shirt", 899, "shirt", "Comfortable formal shirt for office, events and everyday wear."),
    ("Men", "Everyday T-Shirt", 499, "tshirt", "Soft casual T-shirt with a relaxed fit."),
    ("Men", "Slim Fit Jeans", 1199, "jeans", "Versatile denim jeans for daily styling."),
    ("Men", "Casual Jacket", 1799, "jacket", "Layer up with a stylish everyday jacket."),
    ("Men", "Traditional Kurta", 999, "kurta", "Traditional kurta for celebrations and family occasions."),
    ("Men", "Classic Blazer", 2499, "blazer", "A smart blazer for formal and party looks."),
]:
    add("Fashion", sub, name, price, img, desc)

# Fashion - women
for sub, name, price, img, desc in [
    ("Women", "Printed Kurti", 799, "saree", "A colourful kurti for everyday and festive wear."),
    ("Women", "Women's Jeans", 1199, "jeans", "Easy-to-style denim for casual outfits."),
    ("Women", "Crop Top", 599, "crop", "Trendy crop top for casual styling."),
    ("Women", "Bodycon Dress", 1399, "dress", "A sleek bodycon dress for outings and parties."),
    ("Women", "Elegant Saree", 1899, "saree", "Traditional saree for celebrations and special occasions."),
    ("Women", "Festive Lehenga", 2999, "lehenga", "Festive lehenga-inspired outfit for special events."),
    ("Women", "Anarkali Gown", 2199, "dress", "Flowing Anarkali-style gown for festive occasions."),
]:
    add("Fashion", sub, name, price, img, desc)

# Mobiles - real brands listed as brand options; illustrative product images
for brand, name, price, img in [
    ("Samsung", "Samsung Galaxy Smartphone", 18999, "phone"),
    ("Vivo", "Vivo Smartphone", 14999, "phone"),
    ("Oppo", "Oppo Smartphone", 15999, "phone"),
    ("Realme", "Realme Smartphone", 12999, "phone"),
    ("iPhone", "Apple iPhone", 59999, "iphone"),
    ("Motorola", "Motorola Smartphone", 13999, "phone"),
]:
    add("Mobiles", brand, name, price, img, f"{brand} mobile listing. Check the seller's official specifications before purchasing.")

# Electronics
for sub, name, price, img, desc in [
    ("Computers", "Everyday Laptop", 42999, "laptop", "Laptop for study, office work and entertainment."),
    ("Displays", "Full HD Monitor", 8999, "monitor", "Monitor for home, study or office setup."),
    ("Office", "Home Office Printer", 6499, "printer", "Printer for common home and office tasks."),
    ("Presentation", "HD Projector", 18999, "projector", "Projector for presentations and home viewing."),
]:
    add("Electronics", sub, name, price, img, desc)

# Accessories
for sub, name, price, img, desc in [
    ("Men", "Men's Everyday Watch", 1499, "watch", "A versatile watch for everyday and formal outfits."),
    ("Women", "Women's Elegant Watch", 1799, "watch", "A stylish watch for casual and occasion wear."),
    ("Unisex", "UV Style Sunglasses", 799, "sunglasses", "Fashion sunglasses; verify UV protection on the product label."),
    ("Women", "Fashion Earrings", 499, "earrings", "Decorative earrings for everyday or festive outfits."),
    ("Unisex", "Decorative Keychain", 199, "keychain", "A small gift or key organiser accessory."),
    ("Women", "Necklace Set", 999, "necklace", "Necklace set for festive and party wear."),
    ("Unisex", "Classic Ring", 599, "ring", "Minimal ring accessory for daily styling."),
]:
    add("Accessories", sub, name, price, img, desc)

# 10 toy types
for sub, name, price, img, desc in [
    ("Soft Toys", "Teddy Bear", 599, "teddy", "Soft cuddly teddy bear."),
    ("Building Toys", "Building Blocks Set", 799, "toy", "Build-and-create block set."),
    ("Puzzles", "Jigsaw Puzzle", 349, "puzzle", "Puzzle activity for family play."),
    ("Vehicles", "Toy Car", 299, "toy", "Toy vehicle for pretend-play adventures."),
    ("Dolls", "Fashion Doll", 499, "toy", "Doll for imaginative play."),
    ("Learning Toys", "Alphabet Learning Board", 399, "puzzle", "Learning activity toy for letters and matching."),
    ("Outdoor Toys", "Flying Disc", 199, "toy", "Outdoor play disc for active fun."),
    ("Musical Toys", "Mini Toy Keyboard", 899, "toy", "Beginner-friendly toy keyboard."),
    ("Board Games", "Family Board Game", 699, "puzzle", "Board game for family game nights."),
    ("Remote Control", "Remote Control Car", 1299, "toy", "Remote-control toy car for supervised play."),
]:
    add("Toys", sub, name, price, img, desc)

# Food & healthcare: dry fruits, chocolate, and 8 seed varieties
for sub, name, price, img, desc in [
    ("Dry Fruits", "Premium Almonds (250 g)", 299, "nuts", "Packaged almonds. Check the label for ingredients, allergens and best-before date."),
    ("Dry Fruits", "Cashews (250 g)", 329, "nuts", "Packaged cashews. Check the label for ingredients, allergens and best-before date."),
    ("Dry Fruits", "Pistachios (200 g)", 399, "nuts", "Packaged pistachios. Check the label for ingredients, allergens and best-before date."),
    ("Chocolate", "Dark Chocolate Bar", 199, "chocolate", "Packaged chocolate treat. Check ingredients and allergen information."),
    ("Chocolate", "Milk Chocolate Box", 249, "chocolate", "Packaged milk chocolate. Check ingredients and allergen information."),
    ("Seeds", "Chia Seeds (200 g)", 149, "seeds", "Food-grade chia seeds for recipes and meals."),
    ("Seeds", "Flax Seeds (200 g)", 99, "seeds", "Food-grade flax seeds; follow package storage instructions."),
    ("Seeds", "Pumpkin Seeds (200 g)", 179, "seeds", "Food-grade pumpkin seeds for snacks and recipes."),
    ("Seeds", "Sunflower Seeds (200 g)", 129, "seeds", "Food-grade sunflower seeds for snacks and meals."),
    ("Seeds", "Sesame Seeds (200 g)", 89, "seeds", "Food-grade sesame seeds. Sesame is a common food allergen."),
    ("Seeds", "Watermelon Seeds (200 g)", 149, "seeds", "Food-grade watermelon seeds for recipes and snacking."),
    ("Seeds", "Basil Seeds (200 g)", 119, "seeds", "Food-grade basil seeds; prepare according to the package directions."),
    ("Seeds", "Hemp Seeds (200 g)", 249, "seeds", "Food-grade hemp seeds; check local product labelling and package directions."),
]:
    add("Food & Healthcare", sub, name, price, img, desc)

df = pd.DataFrame(items)
CATEGORIES = ["All Products", "Fashion", "Mobiles", "Electronics", "Accessories", "Toys", "Food & Healthcare"]

# ---------- SESSION STATE ----------
if "cart" not in st.session_state:
    st.session_state.cart = {}
if "wishlist" not in st.session_state:
    st.session_state.wishlist = set()
if "page" not in st.session_state:
    st.session_state.page = "Shop"
if "selected_product" not in st.session_state:
    st.session_state.selected_product = None
if "orders" not in st.session_state:
    st.session_state.orders = []

def money(value):
    return f"₹{value:,.0f}"

def add_to_cart(pid):
    st.session_state.cart[pid] = st.session_state.cart.get(pid, 0) + 1

def product_card(row):
    with st.container():
        st.markdown('<div class="product-card">', unsafe_allow_html=True)
        st.image(row["image"], use_container_width=True)
        st.markdown(f'<div class="product-name">{row["name"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="product-category">{row["category"]} · {row["subcategory"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="price">{money(row["price"])}</div>', unsafe_allow_html=True)
        st.caption(row["description"])
        c1, c2 = st.columns(2)
        if c1.button("＋ Add", key=f"add_{row['id']}", use_container_width=True):
            add_to_cart(row["id"])
            st.toast(f"Added {row['name']} to cart")
        if c2.button("♡ Save", key=f"wish_{row['id']}", use_container_width=True):
            st.session_state.wishlist.add(row["id"])
            st.toast("Added to wishlist")
        if st.button("View details", key=f"detail_{row['id']}", use_container_width=True):
            st.session_state.selected_product = int(row["id"])
            st.session_state.page = "Product Details"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown("# 🛍️ ShopNova")
    st.caption("Colour your everyday shopping")
    page = st.radio(
        "Navigate",
        ["Shop", "Product Details", "Wishlist", "Shopping Cart", "Checkout", "Order History"],
        key="page",
    )
    st.divider()
    st.markdown("### 🧭 Shop by category")
    selected_category = st.selectbox("Category", CATEGORIES, key="category_filter")
    search_text = st.text_input("🔎 Search products", placeholder="Search shirt, iPhone, seeds...")
    st.divider()
    cart_count = sum(st.session_state.cart.values())
    st.metric("🛒 Cart items", cart_count)
    st.metric("♡ Wishlist", len(st.session_state.wishlist))
    st.caption("Demo shopping site · No real payments")

# ---------- HEADER ----------
st.markdown("""
<div class="hero">
  <h1>ShopNova — Shop Your Style ✨</h1>
  <p>Fashion • Mobiles • Electronics • Accessories • Toys • Food & Healthcare</p>
</div>
""", unsafe_allow_html=True)

if page == "Shop":
    st.subheader("🛒 Discover products")
    st.markdown('<span class="pill">🌈 Colourful deals</span><span class="pill">🖤 Dark mode</span><span class="pill">🚚 Demo shopping</span>', unsafe_allow_html=True)

    shown = df.copy()
    if selected_category != "All Products":
        shown = shown[shown["category"] == selected_category]
    if search_text.strip():
        needle = search_text.strip().lower()
        shown = shown[
            shown["name"].str.lower().str.contains(needle, na=False)
            | shown["category"].str.lower().str.contains(needle, na=False)
            | shown["subcategory"].str.lower().str.contains(needle, na=False)
            | shown["description"].str.lower().str.contains(needle, na=False)
        ]

    if selected_category == "Fashion" and not search_text.strip():
        gender = st.radio("Fashion collection", ["All", "Male", "Female"], horizontal=True)
        if gender == "Male":
            shown = shown[shown["subcategory"] == "Men"]
        elif gender == "Female":
            shown = shown[shown["subcategory"] == "Women"]
    elif selected_category == "Mobiles" and not search_text.strip():
        brand_filter = st.selectbox("Choose mobile brand", ["All brands", "Samsung", "Vivo", "Oppo", "Realme", "iPhone", "Motorola"])
        if brand_filter != "All brands":
            shown = shown[shown["subcategory"] == brand_filter]
    elif selected_category in ["Accessories", "Toys", "Food & Healthcare"] and not search_text.strip():
        subs = ["All types"] + sorted(shown["subcategory"].unique().tolist())
        sub_filter = st.selectbox("Filter type", subs)
        if sub_filter != "All types":
            shown = shown[shown["subcategory"] == sub_filter]

    st.caption(f"Showing {len(shown)} product(s)")
    if shown.empty:
        st.warning("No products found. Try another search.")
    else:
        cards = st.columns(3, gap="medium")
        for i, (_, row) in enumerate(shown.iterrows()):
            with cards[i % 3]:
                product_card(row)

elif page == "Product Details":
    pid = st.session_state.selected_product
    if pid is None:
        st.info("Choose a product from Shop and click View details.")
    else:
        row = df[df["id"] == pid].iloc[0]
        left, right = st.columns([1, 1.1], gap="large")
        with left:
            st.image(row["image"], use_container_width=True)
        with right:
            st.markdown(f"## {row['name']}")
            st.markdown(f'<span class="pill">{row["category"]}</span><span class="pill">{row["subcategory"]}</span>', unsafe_allow_html=True)
            st.markdown(f"### <span style='color:#6ee7b7'>{money(row['price'])}</span>", unsafe_allow_html=True)
            st.write(row["description"])
            st.write("**Product information**")
            st.write("- Sample price for demonstration")
            st.write("- Image may be illustrative and may not show the exact model")
            st.write("- Confirm size, specifications, ingredients and seller details before purchase")
            if st.button("🛒 Add to cart", key="detail_add"):
                add_to_cart(pid)
                st.success("Added to cart.")
            if st.button("♡ Add to wishlist", key="detail_wish"):
                st.session_state.wishlist.add(pid)
                st.success("Added to wishlist.")

elif page == "Wishlist":
    st.subheader("♡ Your Wishlist")
    if not st.session_state.wishlist:
        st.info("Your wishlist is empty. Save products from the Shop page.")
    else:
        wish_df = df[df["id"].isin(st.session_state.wishlist)]
        cols = st.columns(3)
        for i, (_, row) in enumerate(wish_df.iterrows()):
            with cols[i % 3]:
                product_card(row)
                if st.button("Remove from wishlist", key=f"remove_wish_{row['id']}"):
                    st.session_state.wishlist.discard(int(row["id"]))
                    st.rerun()

elif page == "Shopping Cart":
    st.subheader("🛒 Your Shopping Cart")
    if not st.session_state.cart:
        st.info("Your cart is empty. Add some products first.")
        if st.button("Continue shopping"):
            st.session_state.page = "Shop"
            st.rerun()
    else:
        total = 0
        for pid, qty in list(st.session_state.cart.items()):
            row = df[df["id"] == pid].iloc[0]
            line_total = int(row["price"]) * qty
            total += line_total
            a, b, c, d = st.columns([1.2, 2.4, 1.3, 1.2])
            with a:
                st.image(row["image"], use_container_width=True)
            with b:
                st.markdown(f"**{row['name']}**")
                st.caption(f"{row['category']} · {money(row['price'])} each")
            with c:
                new_qty = st.number_input("Qty", min_value=1, max_value=20, value=qty, key=f"qty_{pid}")
                st.session_state.cart[pid] = int(new_qty)
            with d:
                st.markdown(f"**{money(line_total)}**")
                if st.button("Remove", key=f"remove_cart_{pid}"):
                    del st.session_state.cart[pid]
                    st.rerun()
            st.divider()
        total = sum(int(df[df["id"] == pid].iloc[0]["price"]) * qty for pid, qty in st.session_state.cart.items())
        st.markdown(f"## Total: <span style='color:#6ee7b7'>{money(total)}</span>", unsafe_allow_html=True)
        st.caption("Delivery charges and taxes are not included in this demo.")
        if st.button("Proceed to checkout", type="primary"):
            st.session_state.page = "Checkout"
            st.rerun()

elif page == "Checkout":
    st.subheader("📦 Checkout")
    if not st.session_state.cart:
        st.info("Your cart is empty.")
    else:
        total = sum(int(df[df["id"] == pid].iloc[0]["price"]) * qty for pid, qty in st.session_state.cart.items())
        st.markdown(f"### Order total: <span style='color:#6ee7b7'>{money(total)}</span>", unsafe_allow_html=True)
        with st.form("checkout_form"):
            customer_name = st.text_input("Full name")
            email = st.text_input("Email address")
            phone = st.text_input("Mobile number")
            address = st.text_area("Delivery address")
            payment = st.selectbox("Payment method", ["Cash on Delivery (Demo)", "UPI (Demo only)", "Card (Demo only)"])
            submitted = st.form_submit_button("Place demo order")
        if submitted:
            if not customer_name.strip() or not phone.strip() or not address.strip():
                st.error("Please fill in your name, mobile number and delivery address.")
            else:
                order = {
                    "order_no": f"SN{len(st.session_state.orders) + 1001}",
                    "name": customer_name, "email": email, "phone": phone,
                    "address": address, "payment": payment, "total": total,
                    "items": [
                        {"name": df[df["id"] == pid].iloc[0]["name"], "qty": qty}
                        for pid, qty in st.session_state.cart.items()
                    ],
                }
                st.session_state.orders.append(order)
                st.session_state.cart = {}
                st.success(f"Demo order placed! Order number: {order['order_no']}")
                st.info("No actual payment has been taken. This is a demonstration checkout.")

elif page == "Order History":
    st.subheader("🧾 Order History")
    if not st.session_state.orders:
        st.info("No orders yet.")
    else:
        for order in reversed(st.session_state.orders):
            with st.expander(f"Order {order['order_no']} · {money(order['total'])}"):
                st.write(f"**Name:** {order['name']}")
                st.write(f"**Payment:** {order['payment']}")
                st.write(f"**Address:** {order['address']}")
                st.write("**Items:**")
                for item in order["items"]:
                    st.write(f"- {item['name']} × {item['qty']}")

st.divider()
st.markdown(
    '<p class="small-note">ShopNova demo store · Product prices are sample prices. Online images are illustrative. '
    'Food products are not medical advice; read packaging, allergens and expiry details before use.</p>',
    unsafe_allow_html=True
)
