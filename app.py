    category = st.selectbox("📂 Category", CATEGORIES)
    search = st.text_input("🔎 Search products", placeholder="Search shirt, iPhone, seeds...")
    max_price = st.slider("💰 Maximum price (₹)", 100, 100000, 100000, step=100)
    st.caption("Product photos are loaded from hosted image URLs. Internet access is needed.")

product_by_id = {p["id"]: p for p in products}

def show_product(p, col):
    with col:
        st.markdown('<div class="product-card">', unsafe_allow_html=True)
        try:
            st.image(p["image"], width="stretch", caption=p["category"])
        except Exception:
            st.info("Image unavailable")
        st.markdown(f'<div class="product-title">{p["name"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="product-meta">{p["description"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="price">₹{p["price"]:,}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        x, y = st.columns(2)
        if x.button("🛒 Add to cart", key=f"cart_{p['id']}", use_container_width=True):
            st.session_state.cart[p["id"]] = st.session_state.cart.get(p["id"], 0) + 1
            st.toast(f"{p['name']} added to cart!")
        wish_label = "💜 Saved" if p["id"] in st.session_state.wishlist else "♡ Wishlist"
        if y.button(wish_label, key=f"wish_{p['id']}", use_container_width=True):
            if p["id"] in st.session_state.wishlist:
                st.session_state.wishlist.remove(p["id"])
                st.toast("Removed from wishlist")
            else:
                st.session_state.wishlist.append(p["id"])
                st.toast("Added to wishlist")

# -------------------- Pages --------------------
if page == "Shop":
    st.subheader("🌈 Explore Products")
    filtered = products
    if category != "All":
        filtered = [p for p in filtered if p["category"] == category]
    if search.strip():
        q = search.lower().strip()
        filtered = [p for p in filtered if q in p["name"].lower() or q in p["description"].lower() or q in p["category"].lower() or q in p["subcategory"].lower()]
    filtered = [p for p in filtered if p["price"] <= max_price]

    if not filtered:
        st.warning("No products found. Try another search or category.")
    else:
        st.caption(f"Showing {len(filtered)} products")
        for start in range(0, len(filtered), 4):
            row = st.columns(4)
            for i, p in enumerate(filtered[start:start+4]):
                show_product(p, row[i])

elif page == "Wishlist":
    st.subheader("💜 Your Wishlist")
    saved = [product_by_id[i] for i in st.session_state.wishlist if i in product_by_id]
    if not saved:
        st.info("Your wishlist is empty. Add products using the Wishlist button.")
    else:
        for start in range(0, len(saved), 3):
            row = st.columns(3)
            for i, p in enumerate(saved[start:start+3]):
                show_product(p, row[i])

elif page == "Cart":
    st.subheader("🛒 Your Shopping Cart")
    if not st.session_state.cart:
        st.info("Your cart is empty. Go to Shop and add some products.")
    else:
        total = 0
        for pid in list(st.session_state.cart.keys()):
            p = product_by_id[pid]
            qty = st.session_state.cart[pid]
            line_total = p["price"] * qty
            total += line_total
            left, mid, right = st.columns([3, 1, 1])
            left.write(f"**{p['name']}**  \n₹{p['price']:,} × {qty} = **₹{line_total:,}**")
            new_qty = mid.number_input("Qty", min_value=1, max_value=99, value=qty, key=f"qty_{pid}")
            st.session_state.cart[pid] = new_qty
            if right.button("Remove", key=f"remove_{pid}"):
                del st.session_state.cart[pid]
                st.rerun()
        st.markdown("---")
        st.markdown(f"## Total: ₹{total:,}")
        customer = st.text_input("Full name")
        address = st.text_area("Delivery address")
        payment = st.selectbox("Payment method", ["Cash on Delivery", "UPI demo", "Card demo"])
        if st.button("✅ Place demo order", use_container_width=True):
            if not customer.strip() or not address.strip():
                st.error("Please enter your name and delivery address.")
            else:
                st.session_state.orders.append({
                    "customer": customer.strip(),
                    "address": address.strip(),
                    "payment": payment,
                    "items": [(product_by_id[i]["name"], q, product_by_id[i]["price"] * q)
                              for i, q in st.session_state.cart.items()],
                    "total": sum(product_by_id[i]["price"] * q for i, q in st.session_state.cart.items())
                })
                st.session_state.cart = {}
                st.success("🎉 Demo order placed successfully!")
                st.info("This is a demo checkout. No real payment is processed.")
                st.rerun()

elif page == "My Orders":
    st.subheader("📦 My Orders")
    if not st.session_state.orders:
        st.info("You have no orders yet.")
    else:
        for i, order in enumerate(reversed(st.session_state.orders), 1):
            with st.expander(f"Order #{len(st.session_state.orders)-i+1} — ₹{order['total']:,}"):
                st.write(f"**Customer:** {order['customer']}")
                st.write(f"**Address:** {order['address']}")
                st.write(f"**Payment:** {order['payment']} (demo)")
                for name, qty, amount in order["items"]:
                    st.write(f"- {name} × {qty} — ₹{amount:,}")
                st.write(f"**Total: ₹{order['total']:,}**")

st.markdown("---")
st.markdown("<center>Made with 💜 using Streamlit · Demo store for learning</center>", unsafe_allow_html=True)
