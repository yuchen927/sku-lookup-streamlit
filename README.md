# SKU Lookup Tool (Google Sheets Version)

This is a Streamlit web app that:
- Loads SKU → Category mappings from a live Google Sheet
- Allows users to search SKUs manually or by file upload
- Adds new SKUs with categories (persistently)
- Downloads results as CSV

## 🔧 Setup

1. Create a Google Sheet with columns:
   ```
   No | No_Category
   ```

2. Create a Service Account via Google Cloud Console.
3. Download `credentials.json` and place it in this project directory.
4. Share your Google Sheet with the service account email.

## ▶️ Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 🔐 File Required

Place your downloaded `credentials.json` in the root folder before running.
