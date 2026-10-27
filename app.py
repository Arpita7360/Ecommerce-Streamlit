
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="ShopEase | Online Shopping",
    page_icon="🛍️",
    layout="wide"
)

# -------------------- PRODUCTS --------------------
PRODUCTS = [
    {
        "id": 1,
        "name": "Wireless Headphones",
        "category": "Electronics",
        "price": 1499,
        "emoji": "🎧",
        "description": "Comfortable wireless headphones with rich sound."
    },
    {
        "id": 2,
        "name": "Smart Watch",
        "category": "Electronics",
        "price": 2199,
        "emoji": "⌚",
        "description": "A stylish watch for everyday activities."
    },
    {
        "id": 3,
        "name": "Running Shoes",
        "category": "Fashion",
        "price": 1799,
        "emoji": "👟",
        "description": "Lightweight shoes for walking and running."
    },
    {
        "id": 4,
        "name": "Casual T-Shirt",
        "category": "Fashion",
        "price": 599,
        "emoji": "👕",
        "description": "A comfortable everyday cotton T-shirt."
    },
    {
        "id": 5,
        "name": "Travel Backpack",
        "category": "Accessories",
        "price": 999,
        "emoji": "🎒",
        "description": "A practical backpack for travel and college."
    },
    {
        "id": 6,
        "name": "Sunglasses",
        "category": "Accessories",
        "price": 799,
        "emoji": "🕶️",
        "description": "Modern sunglasses for everyday style."
    },
    {
        "id": 7,
        "name": "Coffee Maker",
        "category": "Home",
        "price": 2499,
        "emoji": "☕",
        "description": "Make your favorite coffee at home."
    },
    {
        "id": 8,
        "name": "Desk Lamp",
        "category": "Home",
        "price": 699,
        "emoji": "💡",
        "description": "A useful lamp for studying and working."
    },
]

# -------------------- INITIALIZE SESSION --------------------
if "cart" not in st.session_state:
    st.session_state.cart = {}

if "orders" not in st.session_state:
    st.session_state.orders = []

if "page" not in st.session_state:
    st.session_state.page = "Home"


def money(amount):
    return f"₹{amount:,.2f}"


def add_to_cart(product_id):
    cart = st.session_state.cart
    cart[product_id] = cart.get(product_id, 0) + 1


def cart_total():
    total = 0
    for product_id, quantity in st.session_state.cart.items():
        product = next(
            p for p in PRODUCTS if p["id"] == product_id
        )
        total += product["price"] * quantity
    return total


# -------------------- CUSTOM STYLE --------------------
st.markdown("""
<style>
    .main-title {
        font-size: 38px;
        font-weight: 800;
        color: #2563eb;
    }
    .subtitle {
        color: #64748b;
        font-size: 17px;
    }
    .product-box {
        padding: 15px;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        background-color: #ffffff;
        margin-bottom: 10px;
    }
    div.stButton > button {
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)


# -------------------- SIDEBAR NAVIGATION --------------------
with st.sidebar:
    st.markdown("# 🛍️ ShopEase")
    st.caption("Your online shopping destination")

    if st.button("🏠 Home", use_container_width=True):
        st.session_state.page = "Home"

    if st.button("🛒 Shopping Cart", use_container_width=True):
        st.session_state.page = "Cart"

    if st.button("📦 My Orders", use_container_width=True):
        st.session_state.page = "Orders"

    st.divider()

    item_count = sum(st.session_state.cart.values())
    st.metric("Cart Items", item_count)
    st.metric("Cart Total", money(cart_total()))


# -------------------- HOME PAGE --------------------
if st.session_state.page == "Home":
    st.markdown(
        '<div class="main-title">Welcome to ShopEase!</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="subtitle">'
        'Discover products for your everyday needs.'
        '</div>',
        unsafe_allow_html=True
    )

    st.write("")
    st.info(
        "🎉 Explore our collection and add your favorite "
        "products to the shopping cart!"
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("Products Available", len(PRODUCTS))
    col2.metric(
        "Categories",
        len(set(p["category"] for p in PRODUCTS))
    )
    col3.metric("Cart Items", sum(st.session_state.cart.values()))

    st.divider()
    st.header("🛍️ Shop Our Products")

    search = st.text_input(
        "🔍 Search products",
        placeholder="Search headphones, shoes, watch..."
    )

    categories = ["All"] + sorted(
        set(p["category"] for p in PRODUCTS)
    )

    selected_category = st.selectbox(
        "Choose a category",
        categories
    )

    filtered_products = PRODUCTS.copy()

    if search:
        filtered_products = [
            p for p in filtered_products
            if search.lower() in p["name"].lower()
            or search.lower() in p["description"].lower()
            or search.lower() in p["category"].lower()
        ]

    if selected_category != "All":
        filtered_products = [
            p for p in filtered_products
            if p["category"] == selected_category
        ]

    if not filtered_products:
        st.warning("No products found. Try another search.")
    else:
        columns = st.columns(3)

        for index, product in enumerate(filtered_products):
            with columns[index % 3]:
                with st.container(border=True):
                    st.markdown(
                        f"<div style='text-align:center;"
                        f"font-size:65px'>{product['emoji']}</div>",
                        unsafe_allow_html=True
                    )
                    st.subheader(product["name"])
                    st.caption(product["category"])
                    st.write(product["description"])
                    st.markdown(
                        f"### {money(product['price'])}"
                    )

                    if st.button(
                        "➕ Add to Cart",
                        key=f"add_{product['id']}",
                        use_container_width=True
                    ):
                        add_to_cart(product["id"])
                        st.toast(
                            f"{product['name']} added to cart!"
                        )


# -------------------- CART PAGE --------------------
elif st.session_state.page == "Cart":
    st.title("🛒 Your Shopping Cart")

    cart = st.session_state.cart

    if not cart:
        st.info("Your cart is empty. Visit Home to shop.")
        if st.button("Continue Shopping"):
            st.session_state.page = "Home"
            st.rerun()
    else:
        for product_id in list(cart.keys()):
            product = next(
                p for p in PRODUCTS if p["id"] == product_id
            )

            col1, col2, col3, col4 = st.columns(
                [3, 2, 2, 1]
            )

            with col1:
                st.write(
                    f"{product['emoji']} **{product['name']}**"
                )
                st.caption(money(product["price"]) + " each")

            with col2:
                new_quantity = st.number_input(
                    "Quantity",
                    min_value=0,
                    max_value=99,
                    value=cart[product_id],
                    step=1,
                    key=f"qty_{product_id}"
                )

                if new_quantity != cart[product_id]:
                    if new_quantity == 0:
                        del st.session_state.cart[product_id]
                    else:
                        st.session_state.cart[product_id] = new_quantity
                    st.rerun()

            with col3:
                st.write(
                    "**Subtotal**",
                    money(product["price"] * cart[product_id])
                )

            with col4:
                if st.button(
                    "🗑️",
                    key=f"remove_{product_id}",
                    help="Remove this product"
                ):
                    del st.session_state.cart[product_id]
                    st.rerun()

            st.divider()

        total = cart_total()
        st.subheader(f"Total: {money(total)}")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Continue Shopping", use_container_width=True):
                st.session_state.page = "Home"
                st.rerun()

        with col2:
            if st.button(
                "Proceed to Checkout",
                type="primary",
                use_container_width=True
            ):
                st.session_state.page = "Checkout"
                st.rerun()


# -------------------- CHECKOUT PAGE --------------------
elif st.session_state.page == "Checkout":
    st.title("📦 Checkout")

    if not st.session_state.cart:
        st.warning("Your cart is empty. Add products first.")
        if st.button("Go Shopping"):
            st.session_state.page = "Home"
            st.rerun()
    else:
        st.write("Enter your details to place a demo order.")
        st.write("Order total:", money(cart_total()))

        with st.form("checkout_form"):
            customer_name = st.text_input("Full Name")
            email = st.text_input("Email Address")
            phone = st.text_input("Phone Number")
            address = st.text_area("Delivery Address")

            submitted = st.form_submit_button(
                "Place Demo Order",
                type="primary"
            )

        if submitted:
            if not all([
                customer_name.strip(),
                email.strip(),
                phone.strip(),
                address.strip()
            ]):
                st.error("Please fill in all the fields.")
            elif "@" not in email or "." not in email.split("@")[-1]:
                st.error("Please enter a valid email address.")
            else:
                order_items = []

                for product_id, quantity in st.session_state.cart.items():
                    product = next(
                        p for p in PRODUCTS
                        if p["id"] == product_id
                    )
                    order_items.append({
                        "Product": product["name"],
                        "Quantity": quantity,
                        "Unit Price": product["price"],
                        "Subtotal": product["price"] * quantity
                    })

                order = {
                    "Order Number": len(st.session_state.orders) + 1,
                    "Customer": customer_name.strip(),
                    "Email": email.strip(),
                    "Phone": phone.strip(),
                    "Address": address.strip(),
                    "Items": order_items,
                    "Total": cart_total()
                }

                st.session_state.orders.append(order)
                st.session_state.cart = {}
                st.session_state.page = "Orders"

                st.success(
                    f"Demo order #{order['Order Number']} placed!"
                )
                st.rerun()


# -------------------- ORDER HISTORY --------------------
elif st.session_state.page == "Orders":
    st.title("📦 My Orders")

    if not st.session_state.orders:
        st.info(
            "You haven't placed any orders in this session yet."
        )
    else:
        for order in reversed(st.session_state.orders):
            with st.expander(
                f"Order #{order['Order Number']} — "
                f"{money(order['Total'])}"
            ):
                st.write("Customer:", order["Customer"])
                st.write("Email:", order["Email"])
                st.write("Delivery address:", order["Address"])

                order_df = pd.DataFrame(order["Items"])
                st.dataframe(
                    order_df,
                    use_container_width=True,
                    hide_index=True
                )

                st.write("**Total:**", money(order["Total"]))

    if st.button("Continue Shopping"):
        st.session_state.page = "Home"
        st.rerun()


# -------------------- FOOTER --------------------
st.divider()
st.caption(
    "ShopEase E-Commerce Demo | Built with Python and Streamlit. "
    "Orders are stored in session memory; no real payments are processed."
)
