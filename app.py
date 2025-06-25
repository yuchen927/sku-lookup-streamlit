import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
from io import StringIO

# Load credentials from Streamlit Secrets
creds_dict = json.loads(st.secrets["GOOGLE_SHEETS_CREDS"])
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(credentials)

# Open the Google Sheet
SHEET_ID = "1EooOFIU6-rBHFPjabKrHB8kw7LyuhHXhsIUN138pLUE"
sheet = client.open_by_key(SHEET_ID).sheet1


# Load existing data
data = sheet.get_all_records()
df = pd.DataFrame(data)

# Session state to track updated DataFrame
if "sku_df" not in st.session_state:
    st.session_state.sku_df = df

sku_dict = dict(zip(st.session_state.sku_df["No"].astype(str), st.session_state.sku_df["No_Category"]))

# Streamlit UI
st.set_page_config(page_title="SKU Lookup Tool", layout="centered")
st.title("🔍 SKU Lookup Tool (Google Sheets)")
st.markdown("Search by typing SKUs or uploading a file. You can also add new SKUs.")

# Search input
sku_input = st.text_input("Enter SKUs (comma separated):", "")

# File upload
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

# Search results
if sku_list:
    results = [sku_dict.get(sku, "SKU Not Found") for sku in sku_list]
    result_df = pd.DataFrame({"SKU": sku_list, "Category": results})
    st.dataframe(result_df, use_container_width=True)

    # CSV download
    csv_buffer = StringIO()
    result_df.to_csv(csv_buffer, index=False)
    st.download_button(
        label="📥 Download Results as CSV",
        data=csv_buffer.getvalue(),
        file_name="sku_lookup_results.csv",
        mime="text/csv"
    )

# Add new SKU
st.markdown("---")
st.header("➕ Add New SKU")

new_sku = st.text_input("Enter new SKU (No)")
new_category = st.text_input("Enter category (No_Category)")

if st.button("Add SKU"):
    if not new_sku.strip():
        st.warning("⚠️ SKU cannot be empty.")
    else:
        # 🧼 Always fetch fresh data before duplicate check
        fresh_records = sheet.get_all_records()
        existing_skus = [row.get("No", "").strip() for row in fresh_records]

        if new_sku.strip() in existing_skus:
            st.warning("⚠️ This SKU already exists.")
        else:
            sheet.append_row([new_sku.strip(), new_category.strip()])
            st.success(f"✅ Added SKU: {new_sku} with category: {new_category}")
            st.rerun()


# Delete existed SKU
st.header("🗑️ Delete SKU From Database")
sku_to_delete = st.text_input("Enter the SKU (No) you want to delete:")

if st.button("Delete SKU"):
    if not sku_to_delete.strip():
        st.warning("⚠️ Please enter a valid SKU.")
    else:
        records = sheet.get_all_records()
        rows_to_delete = [i for i, row in enumerate(records) if str(row.get('No', '')).strip() == sku_to_delete.strip()]

        if rows_to_delete:
            for i in reversed(rows_to_delete):
                sheet.delete_rows(i + 2)  # +2 accounts for header row
            st.success(f"✅ Deleted {len(rows_to_delete)} row(s) with No = '{sku_to_delete}'")
            
            # 👉 This is where you put it:
            st.rerun()  # ✅ FORCE app to re-run from top
        else:
            st.error(f"❌ No match found for '{sku_to_delete}' in the 'No' column.")
