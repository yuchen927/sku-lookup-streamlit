import streamlit as st
import pandas as pd
import os
from io import StringIO

st.set_page_config(page_title="SKU Lookup Tool", layout="centered")

# Load the CSV mapping
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
st.markdown("Search by typing SKUs or uploading a file.")

# Option 1: Manual input
sku_input = st.text_input("Enter SKUs (comma separated):", "")

# Option 2: File upload
uploaded_file = st.file_uploader("OR Upload CSV/Excel with SKU column", type=["csv", "xlsx"])

sku_list = []

if uploaded_file:
    try:
        if uploaded_file.name.endswith(".csv"):
            file_df = pd.read_csv(uploaded_file)
        else:
            file_df = pd.read_excel(uploaded_file)
        if "SKU" not in file_df.columns:
            st.error("File must contain a 'SKU' column.")
        else:
            sku_list = file_df["SKU"].astype(str).tolist()
    except Exception as e:
        st.error(f"Error reading file: {e}")
elif sku_input:
    sku_list = [sku.strip() for sku in sku_input.split(",") if sku.strip()]

# Lookup and show results
if sku_list:
    results = [sku_dict.get(sku, "SKU Not Found") for sku in sku_list]
    result_df = pd.DataFrame({"SKU": sku_list, "Category": results})
    st.dataframe(result_df, use_container_width=True)

    # Export results
    csv_buffer = StringIO()
    result_df.to_csv(csv_buffer, index=False)
    st.download_button(
        label="📥 Download Results as CSV",
        data=csv_buffer.getvalue(),
        file_name="sku_lookup_results.csv",
        mime="text/csv"
    )
