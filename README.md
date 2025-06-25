# SKU Lookup Tool (Google Sheets + Streamlit Secrets)

This version uses Streamlit Cloud **Secrets Management** for secure Google Sheets integration.

## ✅ Features
- Read SKU → Category from live Google Sheet
- Search by typing or uploading file
- Add new SKUs with categories (saved to Google Sheets)
- Download search results as CSV

## 🔒 Setup

1. On [Streamlit Cloud](https://streamlit.io/cloud), open your app and click **Edit Secrets**
2. Paste your `credentials.json` content into secrets like this:

```toml
GOOGLE_SHEETS_CREDS = """<your full json>"""
```

3. Share your Google Sheet with your service account email.

## ▶️ Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```
