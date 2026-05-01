import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# -----------------------------------------------------------------------------
# Page Configuration
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="E-Commerce Analytics",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# Custom CSS for Premium Styling
# -----------------------------------------------------------------------------
def inject_custom_css():
    st.markdown("""
        <style>
        /* Main background and text */
        .stApp {
            background-color: #0E1117;
            color: #FAFAFA;
        }
        
        /* Headers */
        h1, h2, h3 {
            color: #00ADB5 !important;
            font-family: 'Inter', sans-serif;
            font-weight: 600;
        }
        
        /* Metric Cards */
        [data-testid="stMetricValue"] {
            font-size: 28px !important;
            color: #F8B500 !important;
            font-weight: bold;
        }
        [data-testid="stMetricLabel"] {
            font-size: 14px !important;
            color: #A0AAB2 !important;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        [data-testid="metric-container"] {
            background: rgba(30, 34, 41, 0.6);
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.05);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        [data-testid="metric-container"]:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0,173,181,0.2);
        }
        
        /* DataFrame Styling */
        [data-testid="stDataFrame"] {
            border-radius: 10px;
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        /* Expander */
        .streamlit-expanderHeader {
            background-color: rgba(30, 34, 41, 0.8) !important;
            border-radius: 8px !important;
            font-weight: bold !important;
        }
        
        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #1A1F2B;
            border-right: 1px solid rgba(255, 255, 255, 0.05);
        }
        
        /* Custom Title Gradient */
        .gradient-text {
            background: linear-gradient(90deg, #00ADB5, #F8B500);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 42px;
            font-weight: 800;
            margin-bottom: 0px;
        }
        
        /* Separator */
        hr {
            border-color: rgba(255, 255, 255, 0.1);
            margin: 30px 0;
        }
        </style>
    """, unsafe_allow_html=True)

inject_custom_css()

# -----------------------------------------------------------------------------
# Data Loading & Caching
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('Cleaned_df.csv')
        df['order_date'] = pd.to_datetime(df['order_date'])
        df['delivery_date'] = pd.to_datetime(df['delivery_date'])
        
        # Calculate derived metrics if not present
        if 'delivery_time_days' not in df.columns:
            df['delivery_time_days'] = (df['delivery_date'] - df['order_date']).dt.days
            
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.warning("No data available. Please ensure 'Cleaned_df.csv' is in the directory.")
    st.stop()

# -----------------------------------------------------------------------------
# Sidebar Filters
# -----------------------------------------------------------------------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3081/3081840.png", width=60)
    st.markdown("## ⚙️ Filter Dashboard")
    st.markdown("Customize your view by adjusting the parameters below.")
    
    # Date Filter
    min_date = df['order_date'].min().date()
    max_date = df['order_date'].max().date()
    
    date_range = st.date_input(
        "📅 Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Category Filters
    product_types = ["All"] + list(df['product_type'].dropna().unique())
    selected_product_type = st.selectbox("📦 Product Type", product_types)
    
    states = ["All"] + list(df['state'].dropna().unique())
    selected_state = st.selectbox("🗺️ Region / State", states)
    
    genders = ["All"] + list(df['gender'].dropna().unique())
    selected_gender = st.selectbox("👥 Gender", genders)
    
    st.markdown("---")
    st.markdown("### 📊 Quick Dataset Info")
    st.info(f"Total Records: **{len(df):,}**\n\nTotal Features: **{df.shape[1]}**")

# -----------------------------------------------------------------------------
# Data Filtering Logic
# -----------------------------------------------------------------------------
# Apply Date Filter
if len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = df[(df['order_date'].dt.date >= start_date) & (df['order_date'].dt.date <= end_date)]
else:
    filtered_df = df.copy()

# Apply Categorical Filters
if selected_product_type != "All":
    filtered_df = filtered_df[filtered_df['product_type'] == selected_product_type]

if selected_state != "All":
    filtered_df = filtered_df[filtered_df['state'] == selected_state]

if selected_gender != "All":
    filtered_df = filtered_df[filtered_df['gender'] == selected_gender]

if filtered_df.empty:
    st.warning("⚠️ No data matches the selected filters. Please adjust your criteria.")
    st.stop()

# -----------------------------------------------------------------------------
# Header Section
# -----------------------------------------------------------------------------
st.markdown('<p class="gradient-text">🛍️ E-Commerce Executive Dashboard</p>', unsafe_allow_html=True)
st.markdown("*A comprehensive overview of sales performance, customer demographics, and product trends.*")
st.markdown("<br>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Top Row: KPI Metrics
# -----------------------------------------------------------------------------
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

total_revenue = filtered_df['total_price'].sum()
total_orders = filtered_df['sales_id'].nunique()
avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
unique_customers = filtered_df['customer_name'].nunique()

with kpi1:
    st.metric("💰 Total Revenue", f"${total_revenue:,.2f}")
with kpi2:
    st.metric("🛒 Total Orders", f"{total_orders:,}")
with kpi3:
    st.metric("📈 Avg Order Value", f"${avg_order_value:,.2f}")
with kpi4:
    st.metric("👥 Unique Customers", f"{unique_customers:,}")

st.markdown("<hr>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Main Visualization: Revenue Trend
# -----------------------------------------------------------------------------
st.markdown("### 📉 Revenue Trend Over Time")

# Group by day
daily_revenue = filtered_df.groupby(filtered_df['order_date'].dt.date)['total_price'].sum().reset_index()

fig_trend = px.area(
    daily_revenue, 
    x='order_date', 
    y='total_price',
    color_discrete_sequence=['#00ADB5']
)
fig_trend.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font_color='#A0AAB2',
    margin=dict(l=0, r=0, t=20, b=0),
    xaxis_title="",
    yaxis_title="Revenue ($)",
    hovermode="x unified"
)
fig_trend.update_traces(fillcolor='rgba(0,173,181,0.3)', line=dict(width=3))
st.plotly_chart(fig_trend, use_container_width=True)

# -----------------------------------------------------------------------------
# Secondary Section: 2-Column Grid
# -----------------------------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🏆 Top Product Categories")
    prod_rev = filtered_df.groupby('product_type')['total_price'].sum().sort_values(ascending=True).reset_index()
    
    fig_bar = px.bar(
        prod_rev, 
        x='total_price', 
        y='product_type', 
        orientation='h',
        color='total_price',
        color_continuous_scale=['#1A1F2B', '#00ADB5', '#F8B500']
    )
    fig_bar.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#A0AAB2',
        coloraxis_showscale=False,
        xaxis_title="Revenue ($)",
        yaxis_title="",
        margin=dict(l=0, r=0, t=20, b=0)
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    st.markdown("### 🗺️ Sales Distribution by Region")
    state_rev = filtered_df.groupby('state')['total_price'].sum().reset_index()
    
    fig_donut = px.pie(
        state_rev, 
        values='total_price', 
        names='state', 
        hole=0.6,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_donut.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#A0AAB2',
        margin=dict(l=0, r=0, t=20, b=0),
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
    )
    fig_donut.update_traces(textposition='inside', textinfo='percent')
    st.plotly_chart(fig_donut, use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Third Section: Demographics & Price Analysis
# -----------------------------------------------------------------------------
col3, col4 = st.columns(2)

with col3:
    st.markdown("### 👥 Customer Age Distribution")
    if 'age group' in filtered_df.columns:
        age_dist = filtered_df['age group'].value_counts().reset_index()
        age_dist.columns = ['Age Group', 'Count']
        fig_age = px.bar(
            age_dist, 
            x='Age Group', 
            y='Count',
            color='Age Group',
            color_discrete_sequence=['#00ADB5', '#F8B500', '#FF6B6B', '#4ECDC4']
        )
        fig_age.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#A0AAB2',
            showlegend=False,
            margin=dict(l=0, r=0, t=20, b=0)
        )
        st.plotly_chart(fig_age, use_container_width=True)
    else:
        st.info("Age group data not available.")

with col4:
    st.markdown("### 🏷️ Price vs Quantity Ordered")
    # Using a sample if data is large to prevent lag
    sample_df = filtered_df.sample(n=min(1000, len(filtered_df)), random_state=42)
    fig_scatter = px.scatter(
        sample_df, 
        x='price_per_unit', 
        y='quantity', 
        size='total_price',
        color='product_type',
        opacity=0.7,
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig_scatter.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#A0AAB2',
        xaxis_title="Price Per Unit ($)",
        yaxis_title="Quantity",
        margin=dict(l=0, r=0, t=20, b=0),
        legend_title="Product Type"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Insights Summary (Auto-generated)
# -----------------------------------------------------------------------------
st.markdown("### 💡 AI-Generated Insights")
with st.container():
    st.markdown(f"""
    <div style="background-color: rgba(0, 173, 181, 0.1); border-left: 4px solid #00ADB5; padding: 15px; border-radius: 5px;">
        <ul style="margin: 0; color: #E0E6ED;">
            <li><b>Top Performance:</b> Based on current filters, <b>{prod_rev.iloc[-1]['product_type'] if not prod_rev.empty else 'N/A'}</b> is the highest revenue-generating product category.</li>
            <li><b>Regional Spotlight:</b> <b>{state_rev.sort_values(by='total_price', ascending=False).iloc[0]['state'] if not state_rev.empty else 'N/A'}</b> leads in total sales volume.</li>
            <li><b>Customer Behavior:</b> The average order value sits at a healthy <b>${avg_order_value:.2f}</b> across {total_orders:,} transactions.</li>
            <li><b>Data Scope:</b> You are viewing data for <b>{unique_customers:,}</b> unique customers across {len(filtered_df):,} total records.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Data Explorer
# -----------------------------------------------------------------------------
with st.expander("🔍 Explore Raw Data"):
    st.markdown("Filter and sort the raw dataset below:")
    st.dataframe(
        filtered_df.style.background_gradient(cmap='viridis', subset=['total_price'])\
                       .format({'total_price': '${:.2f}', 'price_per_unit': '${:.2f}'}),
        use_container_width=True,
        height=400
    )
    
    # Download button
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv,
        file_name='ecommerce_filtered_data.csv',
        mime='text/csv',
    )

# -----------------------------------------------------------------------------
# Footer
# -----------------------------------------------------------------------------
st.markdown("""
    <div style="text-align: center; color: #A0AAB2; padding-top: 30px; font-size: 12px;">
        <p>Built with ❤️ using Streamlit & Plotly | Data Source: Cleaned_df.csv</p>
    </div>
""", unsafe_allow_html=True)