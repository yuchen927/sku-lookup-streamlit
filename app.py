import streamlit as st
import pandas as pd
import os
from io import StringIO

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
st.markdown("Enter one or more SKUs (comma separated). Example: `10-271, 105-751`")

sku_input = st.text_input("SKU(s)", "")

if sku_input:
    sku_list = [sku.strip() for sku in sku_input.split(",") if sku.strip()]
    results = [sku_dict.get(sku, "SKU Not Found") for sku in sku_list]

    result_df = pd.DataFrame({
        "SKU": sku_list,
        "Category": results
    })

    st.dataframe(result_df, use_container_width=True)

    # Download CSV button
    csv_buffer = StringIO()
    result_df.to_csv(csv_buffer, index=False)
    st.download_button(
        label="📥 Download Results as CSV",
        data=csv_buffer.getvalue(),
        file_name="sku_lookup_results.csv",
        mime="text/csv"
    )
