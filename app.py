import streamlit as st
import pandas as pd
from urllib.parse import quote

st.set_page_config(
    page_title="ColorCart | Online Shopping",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------- COLOURFUL WEBSITE THEME --------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}
.stApp {
    background: linear-gradient(135deg, #fff7ed 0%, #fdf2f8 45%, #eff6ff 100%);
    color: #1f2937;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #6d28d9 0%, #db2777 55%, #f97316 100%);
}
[data-testid="stSidebar"] * { color: white !important; }
.hero {
    padding: 34px 30px;
    border-radius: 24px;
    background: linear-gradient(115deg, #7c3aed, #db2777, #f97316);
    color: white;
    box-shadow: 0 12px 30px rgba(124,58,237,.22);
    margin-bottom: 22px;
}
.hero h1 { font-size: 42px; line-height: 1.15; margin: 0 0 8px 0; color: white; }
.hero p { font-size: 16px; margin: 0; color: white; }
.section-title {
    font-size: 26px; font-weight: 800; color: #5b21b6;
    margin: 16px 0 12px 0;
}
.product-card {
    background: rgba(255,255,255,.96);
    border: 1px solid #f3e8ff;
    border-radius: 18px;
    padding: 12px 13px 15px 13px;
    box-shadow: 0 7px 22px rgba(31,41,55,.08);
    min-height: 100px;
}
.product-name { font-size: 16px; font-weight: 700; color: #312e81; margin: 5px 0; }
.product-meta { font-size: 12px; color: #6b7280; margin-bottom: 5px; }
.product-price { color: #be185d; font-size: 20px; font-weight: 800; }
.pill {
    display: inline-block; border-radius: 999px; padding: 4px 10px;
    background: #f3e8ff; color: #6d28d9; font-size: 11px; font-weight: 700;
}
div.stButton > button {
    border: 0; border-radius: 11px; font-weight: 700;
    background: linear-gradient(90deg, #7c3aed, #db2777);
    color: white; transition: .2s;
}
div.stButton > button:hover {
    border: 0; color: white; transform: translateY(-1px);
    box-shadow: 0 5px 14px rgba(219,39,119,.25);
}
div[data-testid="stMetric"] {
    background: white; padding: 14px; border-radius: 16px;
    border: 1px solid #f3e8ff;
}
hr { border-color: #e9d5ff; }
.small-note { color: #6b7280; font-size: 12px; }
</style>
""", unsafe_allow_html=True)

# -------------------- PRODUCT CATALOG --------------------
# Images are hosted photographs. An internet connection is needed to display them.
# Replace any image URL with your own product photo URL if you prefer.
IMG = {
    "shirt": "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?auto=format&fit=crop&w=800&q=85",
    "tshirt": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?auto=format&fit=crop&w=800&q=85",
    "jeans": "https://images.unsplash.com/photo-1542272604-787c3835535d?auto=format&fit=crop&w=800&q=85",
    "jacket": "https://images.unsplash.com/photo-1551028719-00167b16eac5?auto=format&fit=crop&w=800&q=85",
    "kurta": "https://images.unsplash.com/photo-1610030469983-98e550d6193c?auto=format&fit=crop&w=800&q=85",
    "blazer": "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?auto=format&fit=crop&w=800&q=85",
    "kurti": "https://images.unsplash.com/photo-1583391733956-6c78276477e7?auto=format&fit=crop&w=800&q=85",
    "crop": "https://images.unsplash.com/photo-1566206091558-7f218b696731?auto=format&fit=crop&w=800&q=85",
    "dress": "https://images.unsplash.com/photo-1595777457583-95e059d581b8?auto=format&fit=crop&w=800&q=85",
    "saree": "https://images.unsplash.com/photo-1610030469983-98e550d6193c?auto=format&fit=crop&w=800&q=85",
    "lehenga": "https://images.unsplash.com/photo-1583391733956-6c78276477e7?auto=format&fit=crop&w=800&q=85",
    "phone": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=800&q=85",
    "cover": "https://images.unsplash.com/photo-1603313011101-320f26a4f6f6?auto=format&fit=crop&w=800&q=85",
    "laptop": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&w=800&q=85",
    "monitor": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?auto=format&fit=crop&w=800&q=85",
    "printer": "https://images.unsplash.com/photo-1612815154858-60aa4c59eaa6?auto=format&fit=crop&w=800&q=85",
    "projector": "https://images.unsplash.com/photo-1587825140708-dfaf72ae4b04?auto=format&fit=crop&w=800&q=85",
    "watch": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=800&q=85",
    "sunglasses": "https://images.unsplash.com/photo-1511499767150-a48a237f0083?auto=format&fit=crop&w=800&q=85",
    "earrings": "https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?auto=format&fit=crop&w=800&q=85",
    "necklace": "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?auto=format&fit=crop&w=800&q=85",
    "ring": "https://images.unsplash.com/photo-1605100804763-247f67b3557e?auto=format&fit=crop&w=800&q=85",
    "toy": "https://images.unsplash.com/photo-1596461404969-9ae70f2830c1?auto=format&fit=crop&w=800&q=85",
    "teddy": "https://images.unsplash.com/photo-1559454403-b8fb88521f11?auto=format&fit=crop&w=800&q=85",
    "food": "https://images.unsplash.com/photo-1518843875459-f738682238a6?auto=format&fit=crop&w=800&q=85",
    "chocolate": "https://images.unsplash.com/photo-1511381939415-e44015466834?auto=format&fit=crop&w=800&q=85",
    "seeds": "https://images.unsplash.com/photo-1509358271058-acd22cc93898?auto=format&fit=crop&w=800&q=85",
    "dryfruit": "https://images.unsplash.com/photo-1505576399273-565b52d4ac71?auto=format&fit=crop&w=800&q=85",
}

products = []
def add(category, name, subcategory, price, image, description):
    products.append({
        "id": len(products) + 1, "category": category, "name": name,
        "subcategory": subcategory, "price": int(price), "image": IMG[image],
        "description": description
    })

# Fashion - male
for name, price, key in [
    ("Men's Casual Shirt", 799, "shirt"), ("Men's T-Shirt", 399, "tshirt"),
    ("Men's Denim Jeans", 999, "jeans"), ("Men's Jacket", 1499, "jacket"),
    ("Men's Kurta", 899, "kurta"), ("Men's Blazer", 2499, "blazer")
]:
    add("Fashion", name, "Male", price, key, "Comfortable style for everyday wear and special occasions.")

# Fashion - female
for name, price, key in [
    ("Women's Kurti", 699, "kurti"), ("Women's Jeans", 999, "jeans"),
    ("Women's Crop Top", 499, "crop"), ("Bodycon Dress", 1199, "dress"),
    ("Traditional Saree", 1599, "saree"), ("Designer Lehenga", 2999, "lehenga"),
    ("Anarkali Gown", 2199, "dress")
]:
    add("Fashion", name, "Female", price, key, "A fashionable pick for casual wear, parties, or celebrations.")

# Mobiles and real-photo-style back cover listings
for brand, price in [
    ("Samsung", 18999), ("Vivo", 14999), ("Oppo", 15999),
    ("Realme", 12999), ("iPhone", 59999), ("Motorola", 13999)
]:
    add("Mobiles", f"{brand} Smartphone", brand, price, "phone",
        f"{brand} smartphone listing. Check the seller's exact model and specifications before purchase.")
    add("Mobile Back Covers", f"{brand} Back Cover", brand, 299, "cover",
        f"Protective back cover for selected {brand} phones. Confirm your exact phone model before ordering.")

# Electronics
for name, price, key in [
    ("Laptop", 45999, "laptop"), ("Computer Monitor", 8999, "monitor"),
    ("All-in-One Printer", 6999, "printer"), ("HD Projector", 12999, "projector")
]:
    add("Electronics", name, "Electronics", price, key, "Useful technology for home, study, and office.")

# Accessories
for name, sub, price, key in [
    ("Men's Watch", "Men", 1299, "watch"), ("Women's Watch", "Women", 1499, "watch"),
    ("Sunglasses", "Unisex", 499, "sunglasses"), ("Earrings", "Women", 299, "earrings"),
    ("Keychain", "Unisex", 99, "toy"), ("Necklace Set", "Women", 899, "necklace"),
    ("Fashion Rings", "Unisex", 249, "ring")
]:
    add("Accessories", name, sub, price, key, "A stylish accessory and a useful gift option.")

# Ten different toys
for name, price, key in [
    ("Teddy Bear", 499, "teddy"), ("Building Blocks", 599, "toy"),
    ("Remote Control Car", 899, "toy"), ("Doll Set", 699, "toy"),
    ("Toy Train", 549, "toy"), ("Puzzle Board", 299, "toy"),
    ("Stuffed Animal", 399, "teddy"), ("Toy Robot", 999, "toy"),
    ("Play Kitchen Set", 1199, "toy"), ("Educational Science Kit", 799, "toy")
]:
    add("Toys", name, "Toys", price, key, "Fun playtime item. Check the recommended age on the package.")

# Food and healthcare
add("Food & Healthcare", "Premium Almonds", "Dry Fruits", 499, "dryfruit", "Crunchy almonds for snacking. Check the package for ingredients and allergen information.")
add("Food & Healthcare", "Cashews", "Dry Fruits", 549, "dryfruit", "Cashews for snacks and recipes. Store in a cool, dry place.")
add("Food & Healthcare", "Mixed Dry Fruits", "Dry Fruits", 699, "food", "A mixed selection of dry fruits. Check the label for allergens.")
add("Food & Healthcare", "Dark Chocolate", "Chocolate", 199, "chocolate", "Chocolate treat. Review the ingredients and nutrition label.")
add("Food & Healthcare", "Milk Chocolate", "Chocolate", 149, "chocolate", "Sweet chocolate treat. Review the ingredients and nutrition label.")
for name, price in [
    ("Chia Seeds", 199), ("Flax Seeds", 149), ("Pumpkin Seeds", 249),
    ("Sunflower Seeds", 179), ("Sesame Seeds", 129), ("Watermelon Seeds", 229),
    ("Basil Seeds (Sabja)", 99), ("Hemp Seeds", 349)
]:
    add("Food & Healthcare", name, "Seeds", price, "seeds",
        "Packaged edible seeds. Check the product label, freshness, and allergy information.")

df = pd.DataFrame(products)
CATEGORIES = ["All Products", "Fashion", "Mobiles", "Mobile Back Covers",
              "Electronics", "Accessories", "Toys", "Food & Healthcare"]

# -------------------- SESSION STATE --------------------
if "cart" not in st.session_state:
    st.session_state.cart = {}
if "wishlist" not in st.session_state:
    st.session_state.wishlist = set()
if "page" not in st.session_state:
    st.session_state.page = "Shop"
if "last_order" not in st.session_state:
    st.session_state.last_order = None

# -------------------- HELPERS --------------------
def add_to_cart(product_id):
    st.session_state.cart[product_id] = st.session_state.cart.get(product_id, 0) + 1

def product_by_id(product_id):
    return df[df["id"] == product_id].iloc[0]

def money(amount):
    return f"₹{amount:,.0f}"

def show_product_card(row, column):
    with column:
        st.markdown('<div class="product-card">', unsafe_allow_html=True)
        st.image(row["image"], width="stretch", caption=row["name"])
        st.markdown(f'<div class="pill">{row["category"]} · {row["subcategory"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="product-name">{row["name"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="product-price">{money(row["price"])}</div>', unsafe_allow_html=True)
        st.caption(row["description"])
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🛒 Add", key=f"add_{row['id']}", use_container_width=True):
                add_to_cart(int(row["id"]))
                st.toast(f"{row['name']} added to cart!")
        with c2:
            wish_label = "💜 Saved" if int(row["id"]) in st.session_state.wishlist else "♡ Wishlist"
            if st.button(wish_label, key=f"wish_{row['id']}", use_container_width=True):
                pid = int(row["id"])
                if pid in st.session_state.wishlist:
                    st.session_state.wishlist.remove(pid)
                else:
                    st.session_state.wishlist.add(pid)
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# -------------------- SIDEBAR --------------------
with st.sidebar:
    st.markdown("# 🛍️ ColorCart")
    st.markdown("### Shopping made colourful!")
    st.markdown("---")
    page_choice = st.radio(
        "Navigate",
        ["Shop", "My Cart", "Wishlist", "Checkout"],
        index=["Shop", "My Cart", "Wishlist", "Checkout"].index(st.session_state.page)
        if st.session_state.page in ["Shop", "My Cart", "Wishlist", "Checkout"] else 0
    )
    st.session_state.page = page_choice
    st.markdown("---")
    st.markdown(f"🛒 **Cart items:** {sum(st.session_state.cart.values())}")
    st.markdown(f"💜 **Wishlist:** {len(st.session_state.wishlist)}")
    st.markdown("---")
    st.caption("Demo shopping website. Prices are sample prices.")

# -------------------- HERO --------------------
st.markdown("""
<div class="hero">
  <h1>Find Your Favourite Things ✨</h1>
  <p>Fashion, mobiles, gadgets, accessories, toys and everyday treats — all in one colourful store.</p>
</div>
""", unsafe_allow_html=True)

# -------------------- SHOP PAGE --------------------
if st.session_state.page == "Shop":
    metric1, metric2, metric3 = st.columns(3)
    metric1.metric("Products", len(df))
    metric2.metric("Categories", 7)
    metric3.metric("Cart quantity", sum(st.session_state.cart.values()))

    st.markdown('<div class="section-title">Explore Products</div>', unsafe_allow_html=True)
    f1, f2, f3 = st.columns([1.3, 1, 1])
    with f1:
        search = st.text_input("🔎 Search products", placeholder="Try iPhone, saree, chia seeds...")
    with f2:
        category = st.selectbox("Category", CATEGORIES)
    with f3:
        sort_by = st.selectbox("Sort by", ["Featured", "Price: Low to High", "Price: High to Low", "Name A-Z"])

    filtered = df.copy()
    if category != "All Products":
        filtered = filtered[filtered["category"] == category]
    if search.strip():
        filtered = filtered[
            filtered["name"].str.contains(search.strip(), case=False, na=False)
            | filtered["subcategory"].str.contains(search.strip(), case=False, na=False)
            | filtered["description"].str.contains(search.strip(), case=False, na=False)
        ]
    if category == "Fashion":
        gender = st.radio("Fashion collection", ["All", "Male", "Female"], horizontal=True)
        if gender != "All":
            filtered = filtered[filtered["subcategory"] == gender]
    if category == "Mobiles":
        st.info("Choose a mobile brand above by searching the brand name. Matching back covers are listed under Mobile Back Covers.")
    if sort_by == "Price: Low to High":
        filtered = filtered.sort_values("price")
    elif sort_by == "Price: High to Low":
        filtered = filtered.sort_values("price", ascending=False)
    elif sort_by == "Name A-Z":
        filtered = filtered.sort_values("name")

    st.markdown(f"**Showing {len(filtered)} product(s)**")
    if filtered.empty:
        st.warning("No products found. Try another search.")
    else:
        rows = list(filtered.iterrows())
        for start in range(0, len(rows), 3):
            cols = st.columns(3, gap="large")
            for j, (_, row) in enumerate(rows[start:start + 3]):
                show_product_card(row, cols[j])

# -------------------- CART PAGE --------------------
elif st.session_state.page == "My Cart":
    st.markdown('<div class="section-title">🛒 Your Shopping Cart</div>', unsafe_allow_html=True)
    if not st.session_state.cart:
        st.info("Your cart is empty. Visit Shop and add some products.")
        if st.button("Continue Shopping"):
            st.session_state.page = "Shop"
            st.rerun()
    else:
        total = 0
        for pid in list(st.session_state.cart.keys()):
            row = product_by_id(pid)
            qty = st.session_state.cart[pid]
            line_total = int(row["price"]) * qty
            total += line_total
            image_col, detail_col, qty_col, remove_col = st.columns([1, 3, 1, 1])
            with image_col:
                st.image(row["image"], width=110)
            with detail_col:
                st.markdown(f"**{row['name']}**")
                st.write(f"{money(row['price'])} each")
                st.write(f"Line total: **{money(line_total)}**")
            with qty_col:
                new_qty = st.number_input("Qty", min_value=1, max_value=99, value=qty, key=f"qty_{pid}")
                if new_qty != qty:
                    st.session_state.cart[pid] = int(new_qty)
                    st.rerun()
            with remove_col:
                st.write("")
                if st.button("🗑️ Remove", key=f"remove_{pid}"):
                    del st.session_state.cart[pid]
                    st.rerun()
            st.divider()
        st.markdown(f"### Total: {money(total)}")
        a, b = st.columns(2)
        with a:
            if st.button("Continue Shopping", use_container_width=True):
                st.session_state.page = "Shop"
                st.rerun()
        with b:
            if st.button("Proceed to Checkout", use_container_width=True):
                st.session_state.page = "Checkout"
                st.rerun()

# -------------------- WISHLIST PAGE --------------------
elif st.session_state.page == "Wishlist":
    st.markdown('<div class="section-title">💜 Your Wishlist</div>', unsafe_allow_html=True)
    if not st.session_state.wishlist:
        st.info("No saved products yet. Tap Wishlist on any product card to save it.")
    else:
        saved = df[df["id"].isin(list(st.session_state.wishlist))]
        for start in range(0, len(saved), 3):
            cols = st.columns(3, gap="large")
            for j, (_, row) in enumerate(saved.iloc[start:start + 3].iterrows()):
                show_product_card(row, cols[j])

# -------------------- CHECKOUT PAGE --------------------
elif st.session_state.page == "Checkout":
    st.markdown('<div class="section-title">💳 Checkout</div>', unsafe_allow_html=True)
    if not st.session_state.cart:
        st.info("Your cart is empty. Add products before checkout.")
        if st.button("Go to Shop"):
            st.session_state.page = "Shop"
            st.rerun()
    else:
        total = sum(int(product_by_id(pid)["price"]) * qty for pid, qty in st.session_state.cart.items())
        st.markdown(f"### Order total: {money(total)}")
        st.caption("This is a demo checkout. It does not collect or process real payments.")
        with st.form("checkout_form"):
            customer_name = st.text_input("Full name")
            email = st.text_input("Email address")
            phone = st.text_input("Phone number")
            address = st.text_area("Delivery address")
            payment = st.selectbox("Payment method", ["Cash on Delivery (Demo)", "UPI (Demo)", "Card (Demo)"])
            submitted = st.form_submit_button("Place Demo Order")
        if submitted:
            if not customer_name.strip() or not phone.strip() or not address.strip():
                st.error("Please enter your name, phone number, and delivery address.")
            else:
                order_items = []
                for pid, qty in st.session_state.cart.items():
                    row = product_by_id(pid)
                    order_items.append({
                        "name": row["name"], "quantity": qty,
                        "unit_price": int(row["price"]),
                        "line_total": int(row["price"]) * qty
                    })
                st.session_state.last_order = {
                    "customer": customer_name, "email": email, "phone": phone,
                    "address": address, "payment": payment, "total": total,
                    "items": order_items
                }
                st.session_state.cart = {}
                st.success("🎉 Demo order placed successfully!")
                st.balloons()
                st.markdown("### Order confirmation")
                st.write(f"**Customer:** {customer_name}")
                st.write(f"**Payment:** {payment}")
                st.write(f"**Total:** {money(total)}")
                st.dataframe(pd.DataFrame(order_items), use_container_width=True, hide_index=True)

if st.session_state.last_order and st.session_state.page != "Checkout":
    with st.expander("View your latest demo order"):
        order = st.session_state.last_order
        st.write(f"**Order for:** {order['customer']}")
        st.write(f"**Payment method:** {order['payment']}")
        st.write(f"**Total:** {money(order['total'])}")
        st.dataframe(pd.DataFrame(order["items"]), use_container_width=True, hide_index=True)

st.markdown("---")
st.markdown(
    "<p style='text-align:center;color:#7c3aed;font-weight:700'>ColorCart 🛍️ · Demo E-Commerce Website</p>"
    "<p class='small-note' style='text-align:center'>Product photos load from external image hosts. Sample prices, stock, and checkout are for demonstration only.</p>",
    unsafe_allow_html=True
)
