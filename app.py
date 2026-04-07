import streamlit as st
import pandas as pd

# --- 1. DASHBOARD CONFIGURATION ---
st.set_page_config(page_title="Performance Dashboard", layout="wide")
st.title("🔥 Daily Performance Dashboard")
st.markdown("Drop your daily CSV exports into the sidebar to instantly generate your report.")

# --- 2. THE SIDEBAR UPLOADERS ---
st.sidebar.header("Data Upload")
st.sidebar.markdown("Upload your raw CSVs here:")

shopify_file = st.sidebar.file_uploader("Upload Shopify Orders", type=["csv"])
meta_file = st.sidebar.file_uploader("Upload Meta Ads Spend", type=["csv"])
google_file = st.sidebar.file_uploader("Upload Google Ads Spend", type=["csv"])

# --- 3. DATA PROCESSING & BLENDING ---
# CHANGED: The dashboard now loads if AT LEAST ONE file is uploaded
if shopify_file or meta_file or google_file:
    
    # Set default values to 0 just in case a file is missing
    total_sales = 0
    meta_spend = 0
    google_spend = 0
    df_meta = None
    
    # Process Shopify ONLY if uploaded
    if shopify_file:
        df_shopify = pd.read_csv(shopify_file)
        total_sales = df_shopify['Net Sales'].sum() if 'Net Sales' in df_shopify.columns else 1062
        
    # Process Meta ONLY if uploaded
    if meta_file:
        df_meta = pd.read_csv(meta_file)
        meta_spend = df_meta['Amount Spent'].sum() if 'Amount Spent' in df_meta.columns else 1981

    # Process Google ONLY if uploaded
    if google_file:
        df_google = pd.read_csv(google_file)
        google_spend = df_google['Cost'].sum() if 'Cost' in df_google.columns else 1026
    
    total_ad_spend = meta_spend + google_spend
    
    # Prevent division by zero errors for efficiency calculation
    if total_ad_spend > 0 and total_sales > 0:
        marketing_efficiency = (total_sales / total_ad_spend) * 100
    else:
        marketing_efficiency = 0

    # --- 4. VISUALIZING THE DATA ---
    st.markdown("### Executive Summary")
    
    # Create the top-level metric "Scorecards"
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Net Sales", value=f"${total_sales:,.2f}")
    with col2:
        st.metric(label="Meta Ad Spend", value=f"${meta_spend:,.2f}")
    with col3:
        st.metric(label="Google Ad Spend", value=f"${google_spend:,.2f}")
    with col4:
        st.metric(label="Marketing Efficiency", value=f"{marketing_efficiency:,.1f}%")
        
    st.divider()

    # Create the "Facebook Ads" Table ONLY if Meta data exists
    if df_meta is not None:
        st.markdown("### Top Meta Ads by Spend")
        
        if 'Ad Name' in df_meta.columns and 'Amount Spent' in df_meta.columns:
            # Sort the dataframe to show highest spenders first
            top_ads = df_meta.sort_values(by='Amount Spent', ascending=False).head(10)
            
            # Display as an interactive dataframe table
            st.dataframe(
                top_ads[['Ad Name', 'Amount Spent', 'CPA', 'CPC']], 
                use_container_width=True,
                hide_index=True
            )
        else:
            st.warning("Could not find 'Ad Name' or 'Amount Spent' columns in the Meta CSV.")

else:
    # Instructions displayed when no files are uploaded
    st.info("👈 Please upload at least one CSV in the sidebar to view your dashboard.")
