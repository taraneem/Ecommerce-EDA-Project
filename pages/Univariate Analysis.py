import streamlit as st
import pandas as pd 
import plotly.express as px

# -----------------------------------------------------------------------------
# Page Configuration & CSS
# -----------------------------------------------------------------------------
st.set_page_config(page_title='Univariate Analysis', page_icon="🔬", layout='wide')

def inject_custom_css():
    st.markdown("""
        <style>
        .stApp { background-color: #0E1117; color: #FAFAFA; }
        h1, h2, h3 { color: #00ADB5 !important; font-family: 'Inter', sans-serif; font-weight: 600; }
        .gradient-text {
            background: linear-gradient(90deg, #00ADB5, #F8B500); -webkit-background-clip: text;
            -webkit-text-fill-color: transparent; font-size: 36px; font-weight: 800; margin-bottom: 0px;
        }
        .stTabs [data-baseweb="tab-list"] { background-color: rgba(30, 34, 41, 0.6); border-radius: 8px; padding: 5px; }
        .stTabs [data-baseweb="tab"] { color: #A0AAB2; }
        .stTabs [aria-selected="true"] { background-color: rgba(0, 173, 181, 0.2) !important; color: #00ADB5 !important; border-radius: 5px; }
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

st.markdown('<p class="gradient-text">🔬 Univariate Analysis</p>', unsafe_allow_html=True)
st.markdown("Explore the distribution of individual features within the dataset.")
st.markdown("<br>", unsafe_allow_html=True)

def style_plotly(fig):
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#A0AAB2',
        margin=dict(l=0, r=0, t=40, b=0)
    )
    return fig

# -----------------------------------------------------------------------------
# Tabs
# -----------------------------------------------------------------------------
tab1, tab2, tab3 = st.tabs(['🔢 Numerical Features', '🔠 Categorical Features', '🛠️ Custom Explorer'])

with tab1:
    st.markdown("### Numerical Feature Distributions")
    num_cols = df.select_dtypes(include='number').columns.drop(['sales_id'], errors='ignore')
    
    cols = st.columns(2)
    for i, col in enumerate(num_cols):
        fig = px.histogram(df, x=col, title=f'Distribution of {col}', color_discrete_sequence=['#00ADB5'])
        cols[i % 2].plotly_chart(style_plotly(fig), use_container_width=True)

with tab2:
    st.markdown("### Categorical Feature Distributions")
    cat_cols = df.select_dtypes(include=['object', 'category']).columns.drop(['customer_name', 'order_date', 'delivery_date'], errors='ignore')
    
    cols = st.columns(2)
    for i, col in enumerate(cat_cols):
        fig = px.histogram(df, x=col, text_auto=True, title=f'Distribution of {col}', color_discrete_sequence=['#F8B500'])
        fig.update_xaxes(categoryorder='total descending')
        cols[i % 2].plotly_chart(style_plotly(fig), use_container_width=True)

with tab3:
    st.markdown("### Custom Single Variable Explorer")
    
    col_sel, chart_sel = st.columns(2)
    with col_sel:
        selected_col = st.selectbox('Select Column to Analyze', df.columns)
    with chart_sel:
        chart_type = st.selectbox('Select Chart Type', ['Histogram', 'Pie Chart'])
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("Generate Chart", type="primary"):
        if chart_type == 'Histogram':
            fig = px.histogram(df, x=selected_col, text_auto=True, title=f'Distribution of {selected_col}', color_discrete_sequence=['#00ADB5'])
            st.plotly_chart(style_plotly(fig), use_container_width=True)
        elif chart_type == 'Pie Chart':
            # Count values for pie chart
            pie_df = df[selected_col].value_counts().reset_index()
            pie_df.columns = [selected_col, 'count']
            fig = px.pie(pie_df, names=selected_col, values='count', title=f'Distribution of {selected_col}', hole=0.4, color_discrete_sequence=px.colors.qualitative.Set2)
            st.plotly_chart(style_plotly(fig), use_container_width=True)
