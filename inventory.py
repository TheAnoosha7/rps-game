import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Config ---
st.set_page_config(page_title="Smart Inventory Pro", layout="wide")

# --- Custom Styling for Background & UI ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to right, #f8f9fa, #e9ecef);
    }
    .main-header {
        background-color: #1E3A8A;
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Session State Data ---
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame(columns=["ID", "Product Name", "Category", "Quantity", "Price ($)"])

# --- HEADER ---
st.markdown("<div class='main-header'><h1>📦 SMART INVENTORY MANAGEMENT SYSTEM</h1></div>", unsafe_allow_html=True)

# --- SIDEBAR: OPERATIONAL TOOLS ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/762/762666.png", width=80)
    st.header("Control Center")
    
    with st.expander("✨ Add New Stock", expanded=True):
        id_val = st.text_input("Product ID (e.g. P001)")
        name_val = st.text_input("Item Name")
        cat_val = st.selectbox("Category", ["Electronics", "Furniture", "Apparel", "Stationery"])
        qty_val = st.number_input("Stock Quantity", min_value=0, step=1)
        prc_val = st.number_input("Unit Price ($)", min_value=0.0)
        
        if st.button("Update Database"):
            if id_val and name_val:
                new_entry = pd.DataFrame([[id_val, name_val, cat_val, qty_val, prc_val]], columns=st.session_state.db.columns)
                st.session_state.db = pd.concat([st.session_state.db, new_entry], ignore_index=True)
                st.success("Database Updated!")
            else:
                st.error("Missing Details!")

    if st.button("🗑️ Reset All Records"):
        st.session_state.db = pd.DataFrame(columns=["ID", "Product Name", "Category", "Quantity", "Price ($)"])
        st.rerun()

# --- MAIN DASHBOARD: THE POWERFUL FEATURES ---
col1, col2, col3 = st.columns(3)
total_val = (st.session_state.db["Quantity"] * st.session_state.db["Price ($)"]).sum() if not st.session_state.db.empty else 0

col1.metric("📦 Unique Products", len(st.session_state.db))
col2.metric("🔢 Total Stock Items", int(st.session_state.db["Quantity"].sum()) if not st.session_state.db.empty else 0)
col3.metric("💰 Total Inventory Value", f"${total_val:,.2f}")

st.write("---")

# SEARCH & DATA TABLE
st.subheader("🔍 Search & Filter Inventory")
search = st.text_input("Enter Product Name or ID to filter...")
display_df = st.session_state.db
if search:
    display_df = display_df[display_df["Product Name"].str.contains(search, case=False) | display_df["ID"].str.contains(search, case=False)]

st.dataframe(display_df, use_container_width=True, hide_index=True)

# ANALYTICS CHART
if not st.session_state.db.empty:
    st.write("---")
    st.subheader("📊 Visual Analytics")
    fig = px.bar(st.session_state.db, x="Product Name", y="Quantity", color="Category", title="Current Stock Levels")
    st.plotly_chart(fig, use_container_width=True)

    # DOWNLOAD REPORT
    csv = st.session_state.db.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Official Inventory Report", csv, "report.csv", "text/csv")