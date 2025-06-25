import streamlit as st
import pandas as pd
import os

# Set page title
st.set_page_config(page_title="SKU Lookup Tool", layout="centered")

# Load the CSV file
file_path = "no_category.csv"

@st.cache_data
def load_data():
    if not os.path.exists(file_path):
        return {}
    try:
        df = pd.read_csv(file_path)
        return dict(zip(df["No"].astype(str), df["No_Category"]))
    except Exception as e:
        st.error(f"Failed to load CSV: {e}")
        return {}

sku_dict = load_data()

# UI
st.title("🔍 SKU Lookup Tool")
st.markdown("Enter a SKU to find its category (e.g., `10-271`).")

sku_input = st.text_input("SKU", "")

if sku_input:
    result = sku_dict.get(sku_input.strip(), "SKU Not Found")
    st.success(f"Category: **{result}**")
