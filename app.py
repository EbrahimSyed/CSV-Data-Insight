# Import Libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page Configiration
st.set_page_config(page_title="DataInsight Pro", layout="wide")
st.title("📊 DataInsight Pro")
st.markdown("Upload a CSV file to instantly clean, analyze, and visualize your data.")

# 1. File Uploader
# Ask user to upload a CSV file
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

# If a file is uploaded, then proceed
if uploaded_file is not None:
    # 2. Load Data
    # Read the CSV file into a DataFrame
    df = pd.read_csv(uploaded_file)

    # Data Preprocessing - Example: Convert date columns and sort
    for col in df.columns:
        if 'date' in col.lower():
            df[col] = pd.to_datetime(df[col], errors='coerce')
            df = df.sort_values(by=col)
            st.sidebar.info(f"📅 Sorted by {col}")
    
    # Sidebar - Data Cleaning Options. Example: Remove missing values
    st.sidebar.header("Settings")
    if st.sidebar.checkbox("Remove Missing Values"):
        df = df.dropna()
        st.sidebar.success("Cleaned!")

    # 3. Layout - Tabs for better UX
    tab1, tab2, tab3 = st.tabs(["📋 Data Preview", "📈 Visualization", "🔢 Statistics"])

    # Tab 1: Data Preview, shows the raw dataframe the user uploaded
    with tab1:
        st.subheader("Raw Dataframe")
        st.dataframe(df, use_container_width=True)

    # Tab 2: Visualization, allows user to create visualizations based on the data columns
    # Options for selecting x and y axes and chart type, which are Bar, Line, and Scatter plots
    # Then displays the selected chart
    with tab2:
        st.subheader("Visual Analytics")
        columns = df.columns.tolist()
        
        col1, col2 = st.columns(2)
        with col1:
            x_axis = st.selectbox("Select X-axis", columns)
        with col2:
            y_axis = st.selectbox("Select Y-axis", columns)
            
        chart_type = st.radio("Chart Type", ["Bar", "Line", "Scatter"])

        fig, ax = plt.subplots(figsize=(10, 6)) # Added figsize for better spacing
        
        if chart_type == "Bar":
            sns.barplot(x=df[x_axis], y=df[y_axis], ax=ax)
        elif chart_type == "Line":
            sns.lineplot(x=df[x_axis], y=df[y_axis], ax=ax)
        else:
            sns.scatterplot(x=df[x_axis], y=df[y_axis], ax=ax)
            
        # Rotate the labels so they don't overlap
        plt.xticks(rotation=45, ha='right')
        
        # Adjust layout to make sure nothing is cut off
        plt.tight_layout()
        
        # Display the finished plot
        st.pyplot(fig)

    # Tab 3: Statistics, shows basic statistics of the dataframe using describe()
    with tab3:
        st.subheader("Key Metrics")
        st.write(df.describe())
else:
    st.info("💡 Please upload a CSV file to get started.")