import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Data Explorer", layout="wide")

import base64

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

bg_image = get_base64_of_bin_file("blue.jpg")  # your file name

st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{bg_image}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: white;
    }}

    [data-testid="stSidebar"] {{
        background: rgba(0, 0, 0, 0.6);  /* transparent glass effect */
        backdrop-filter: blur(10px);
        color: white;
    }}

    h1, h2, h3, h4, .stMarkdown {{
        color: #ffffff;
    }}

    .stDataFrame {{
        background-color: rgba(255, 255, 255, 0.08);
        border-radius: 10px;
        padding: 10px;
    }}
    </style>
""", unsafe_allow_html=True)


st.title("📊 Data Explorer")

# Sidebar
st.sidebar.title("Upload Your Data")
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("✅ File loaded successfully!")
    
    # Dataset Info
    st.subheader("🔍 Dataset Preview")
    st.dataframe(df)

    st.subheader("🥸 Dataset Summary")
    st.write(df.describe())

    # Null Values
    st.subheader("❗Missing Values")
    st.write(df.isnull().sum())

    # Column selector
    st.sidebar.subheader("Column to Visualize")
    column = st.sidebar.selectbox("Select a column", df.columns)

    if pd.api.types.is_numeric_dtype(df[column]):
        chart_type = st.sidebar.radio("Chart Type", ["Histogram", "Boxplot"])
        st.subheader(f"📊 {chart_type} of `{column}`")

        if chart_type == "Histogram":
            fig = px.histogram(df, x=column, nbins=20, title=f"Histogram of {column}")
        else:
            fig = px.box(df, y=column, title=f"Boxplot of {column}")
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.subheader(f"⭕ Pie Chart of `{column}`")
        pie_data = df[column].value_counts().reset_index()
        pie_data.columns = [column, "Count"]
        fig = px.pie(pie_data, values='Count', names=column, title=f"Pie Chart of {column}")
        st.plotly_chart(fig, use_container_width=True)

else:
    st.info("📂 Please upload a CSV file to begin.")
