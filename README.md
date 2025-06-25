# SKU Lookup Tool

This is a simple web app to look up SKU categories using Streamlit.

## 🔍 What It Does
Enter an SKU like `10-271`, and the app will return its category (e.g., "Blanks") based on a preloaded CSV.

## 🚀 How to Run (Locally)
1. Clone the repo:
   ```bash
   git clone https://github.com/yourusername/sku-lookup-streamlit.git
   cd sku-lookup-streamlit
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:
   ```bash
   streamlit run app.py
   ```

## 🌐 How to Deploy on Streamlit Cloud
1. Go to [https://streamlit.io/cloud](https://streamlit.io/cloud)
2. Log in with GitHub and click **New App**
3. Choose this repo and set **Main file path** to:
   ```
   app.py
   ```
4. Click **Deploy**

## 📁 Files Included
- `app.py`: Main Streamlit app
- `no_category.csv`: Data file with SKU-to-category mapping
- `requirements.txt`: Python packages

Enjoy your instant SKU search tool!
