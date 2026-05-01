import streamlit as st
import pandas as pd 
import plotly.express as px

# -----------------------------------------------------------------------------
# Page Configuration & CSS
# -----------------------------------------------------------------------------
st.set_page_config(page_title='Marketing Report', page_icon="📢", layout='wide')

def inject_custom_css():
    st.markdown("""
        <style>
        .stApp { background-color: #0E1117; color: #FAFAFA; }
        h1, h2, h3 { color: #00ADB5 !important; font-family: 'Inter', sans-serif; font-weight: 600; }
        .gradient-text {
            background: linear-gradient(90deg, #00ADB5, #F8B500); -webkit-background-clip: text;
            -webkit-text-fill-color: transparent; font-size: 36px; font-weight: 800; margin-bottom: 0px;
        }
        [data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; border: 1px solid rgba(255, 255, 255, 0.1); }
        hr { border-color: rgba(255, 255, 255, 0.1); margin: 30px 0; }
        [data-testid="stSidebar"] { background-color: #1A1F2B; border-right: 1px solid rgba(255, 255, 255, 0.05); }
        </style>
    """, unsafe_allow_html=True)

inject_custom_css()

# -----------------------------------------------------------------------------
# Data Loading
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv('Cleaned_df.csv')
    df['order_date'] = pd.to_datetime(df['order_date']).dt.date
    return df

df = load_data()

st.markdown('<p class="gradient-text">📢 Marketing Report</p>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Sidebar Filters
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## ⚙️ Report Filters")
    
    # Select city
    df_all_cities = ['All Cities'] + df['city'].dropna().unique().tolist()
    selected_city_list = st.multiselect('🏙️ City', df_all_cities, default='All Cities')
    
    # Date filters
    min_dt = df['order_date'].min()
    max_dt = df['order_date'].max()
    
    st.markdown("### 📅 Date Range")
    start_date = st.date_input('Start Date', min_value=min_dt, max_value=max_dt, value=min_dt)
    end_date = st.date_input('End Date', min_value=min_dt, max_value=max_dt, value=max_dt)
    
    st.markdown("### 📊 Chart Settings")
    top_n = st.slider('Top N Products', min_value=5, max_value=30, step=1, value=10)

# -----------------------------------------------------------------------------
# Filtering Data
# -----------------------------------------------------------------------------
if 'All Cities' in selected_city_list or len(selected_city_list) == 0:
    df_filtered = df.copy()
else:
    df_filtered = df[df['city'].isin(selected_city_list)]

df_filtered = df_filtered[(df_filtered['order_date'] >= start_date) & (df_filtered['order_date'] <= end_date)]

# -----------------------------------------------------------------------------
# Display Data & Charts
# -----------------------------------------------------------------------------
st.markdown("### 📋 Filtered Orders Data")
st.dataframe(df_filtered.head(100), use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(f"### 🏆 Top {top_n} Products by Order Count")

plot_df = df_filtered['product_name'].value_counts().reset_index().head(top_n)
plot_df.columns = ['product_name', 'count']

fig = px.bar(
    plot_df, 
    x='product_name', 
    y='count', 
    text_auto=True,
    labels={'product_name': 'Product Name', 'count': 'Number of Orders'},
    color='count',
    color_continuous_scale=['#1A1F2B', '#00ADB5', '#F8B500']
)
fig.update_layout(
    plot_bgcolor='rgba(0,0,0,0)', 
    paper_bgcolor='rgba(0,0,0,0)', 
    font_color='#A0AAB2',
    coloraxis_showscale=False,
    margin=dict(l=0, r=0, t=20, b=0)
)
st.plotly_chart(fig, use_container_width=True)
