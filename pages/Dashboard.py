import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------------------------------------------------------
# Page Configuration & CSS
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Dashboard KPI's", page_icon="📊", layout="wide")

def inject_custom_css():
    st.markdown("""
        <style>
        .stApp { background-color: #0E1117; color: #FAFAFA; }
        h1, h2, h3 { color: #00ADB5 !important; font-family: 'Inter', sans-serif; font-weight: 600; }
        [data-testid="stMetricValue"] { font-size: 28px !important; color: #F8B500 !important; font-weight: bold; }
        [data-testid="stMetricLabel"] { font-size: 14px !important; color: #A0AAB2 !important; text-transform: uppercase; letter-spacing: 1px; }
        [data-testid="metric-container"] {
            background: rgba(30, 34, 41, 0.6); border-radius: 12px; padding: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2); backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.05); transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        [data-testid="metric-container"]:hover { transform: translateY(-5px); box-shadow: 0 8px 25px rgba(0,173,181,0.2); }
        .gradient-text {
            background: linear-gradient(90deg, #00ADB5, #F8B500); -webkit-background-clip: text;
            -webkit-text-fill-color: transparent; font-size: 36px; font-weight: 800; margin-bottom: 0px;
        }
        hr { border-color: rgba(255, 255, 255, 0.1); margin: 30px 0; }
        </style>
    """, unsafe_allow_html=True)

inject_custom_css()

# -----------------------------------------------------------------------------
# Data Loading
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv('Cleaned_df.csv')

df = load_data()

# -----------------------------------------------------------------------------
# KPIs
# -----------------------------------------------------------------------------
st.markdown('<p class="gradient-text">📊 Dashboard KPI\'s</p>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

num_of_customers = df['customer_name'].nunique()
num_of_orders = df['sales_id'].nunique()
total_revenue = df['total_price'].sum() 
average_order_value = df['total_price'].mean()
average_delivery_days = int(df['delivery_days'].mean().round()) if 'delivery_days' in df.columns else 0

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric('Total Customers', f"{num_of_customers:,}")
with col2:
    st.metric('Total Orders', f"{num_of_orders:,}")
with col3:
    st.metric('Total Revenue', f"${total_revenue:,.0f}")
with col4:
    st.metric('Average Revenue', f"${average_order_value:,.2f}")
with col5:
    st.metric('Avg Delivery (Days)', f"{average_delivery_days}")

st.markdown("<hr>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Sales Analysis
# -----------------------------------------------------------------------------
st.markdown("### 📈 Sales Insights")
df_sorted = df.sort_values(by='order_date')

month_line, product_month_line = st.columns(2)

def style_plotly(fig):
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#A0AAB2',
        margin=dict(l=0, r=0, t=40, b=0)
    )
    return fig

with month_line:
    plot_df = df_sorted.groupby('month')['total_price'].sum().reset_index()
    fig1 = px.line(plot_df, x='month', y='total_price', title='Total Revenue per Month', markers=True, color_discrete_sequence=['#00ADB5'])
    st.plotly_chart(style_plotly(fig1), use_container_width=True)

with product_month_line:
    plot_df = df_sorted.groupby(['month', 'product_type'])['total_price'].sum().reset_index()
    fig2 = px.line(plot_df, x='month', y='total_price', title='Revenue per Month by Product', color='product_type', markers=True, color_discrete_sequence=px.colors.qualitative.Set2)
    st.plotly_chart(style_plotly(fig2), use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    plot_df = df.groupby('product_type')['sales_id'].count().sort_values(ascending=False).reset_index()
    fig3 = px.bar(plot_df, x='product_type', y='sales_id', title='Total Orders per Product Category', text_auto=True, color='sales_id', color_continuous_scale=['#1A1F2B', '#00ADB5'])
    fig3.update_layout(coloraxis_showscale=False)
    st.plotly_chart(style_plotly(fig3), use_container_width=True)
    
with col2:
    plot_df = df.groupby('product_type')['total_price'].sum().sort_values(ascending=False).reset_index()
    fig4 = px.bar(plot_df, x='product_type', y='total_price', title='Total Revenue per Product Category', text_auto=True, color='total_price', color_continuous_scale=['#1A1F2B', '#F8B500'])
    fig4.update_layout(coloraxis_showscale=False)
    st.plotly_chart(style_plotly(fig4), use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Customer Analysis
# -----------------------------------------------------------------------------
st.markdown("### 👥 Customer Analysis")

col1, col2 = st.columns(2)

with col1:
    plot_df = df['state'].value_counts(ascending=True).reset_index()
    plot_df.columns = ['state', 'count']
    fig5 = px.bar(plot_df, y='state', x='count', text_auto=True, title='Orders by State', orientation='h', color_discrete_sequence=['#00ADB5'])
    st.plotly_chart(style_plotly(fig5), use_container_width=True)

with col2:
    if 'age group' in df.columns:
        plot_df = df['age group'].value_counts().reset_index()
        plot_df.columns = ['age group', 'count']
        fig6 = px.pie(plot_df, names='age group', values='count', title='Orders per Age Group', hole=0.6, color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(style_plotly(fig6), use_container_width=True)
    else:
        st.info("Age group data not available.")

st.markdown("<hr>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Product Analysis
# -----------------------------------------------------------------------------
st.markdown("### 📦 Product Analysis")

col1, col2 = st.columns(2)

with col1:
    if 'age group' in df.columns:
        plot_df = df.groupby(['colour', 'age group'])['sales_id'].count().reset_index()
        fig7 = px.bar(plot_df, x='colour', y='sales_id', color='age group', barmode='group', title='Orders per Color & Age Group', color_discrete_sequence=px.colors.qualitative.Set2)
        st.plotly_chart(style_plotly(fig7), use_container_width=True)

with col2:
    plot_df = df['size'].value_counts().reset_index()
    plot_df.columns = ['size', 'count']
    fig8 = px.pie(plot_df, names='size', values='count', title='Percentage of Sizes Ordered', hole=0.6, color_discrete_sequence=px.colors.qualitative.Vivid)
    st.plotly_chart(style_plotly(fig8), use_container_width=True)