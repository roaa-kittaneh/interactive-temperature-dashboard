
import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. Page Configuration ---
st.set_page_config(
    page_title="Global Temperature Dashboard",
    page_icon="🌍",
    layout="wide"
)

# --- 2. Data Loading (Cached) ---
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/Steven-Alvarado/Global-Temperature-Analysis/refs/heads/main/GlobalTemperatures.csv"
    df = pd.read_csv(url )
    df['dt'] = pd.to_datetime(df['dt'])
    df['Year'] = df['dt'].dt.year
    df.dropna(subset=['LandAverageTemperature'], inplace=True)
    return df

# Load the data
df = load_data()

# --- 3. App Title and Description ---
st.title("🌍 Global Temperature Trends Dashboard")
st.markdown("Explore how average land temperatures have changed over time. Use the sidebar filters to customize the analysis.")

# --- 4. Sidebar for User Input ---
st.sidebar.header("⚙️ Filters & Options")

# Year Range Slider
year_range = st.sidebar.slider(
    "Select Year Range:",
    min_value=int(df['Year'].min()),
    max_value=int(df['Year'].max()),
    value=(1900, 2015)  # Default range
)

# --- 5. Data Filtering ---
filtered_df = df[
    (df['Year'] >= year_range[0]) &
    (df['Year'] <= year_range[1])
]

# --- 6. Main Page Content ---
st.write(f"## 📈 Temperature Analysis from {year_range[0]} to {year_range[1]}")

# Group data for plotting
yearly_temp = filtered_df.groupby('Year')['LandAverageTemperature'].mean().reset_index()

# --- 7. Chart Display (with enhancements) ---
st.subheader("📊 Average Temperature Plot")

# Chart type selection
chart_type = st.sidebar.radio(
    "Select Chart Type:",
    ("Line Chart", "Bar Chart")
)

# Create the plot based on user selection
if chart_type == "Line Chart":
    fig = px.line(
        yearly_temp,
        x='Year',
        y='LandAverageTemperature',
        title='Global Average Land Temperature Over Time',
        labels={'Year': 'Year', 'LandAverageTemperature': 'Average Temperature (°C)'}
    )
else:  # "Bar Chart"
    fig = px.bar(
        yearly_temp,
        x='Year',
        y='LandAverageTemperature',
        title='Global Average Land Temperature Over Time',
        labels={'Year': 'Year', 'LandAverageTemperature': 'Average Temperature (°C)'}
    )

# Optional: Add a moving average trendline
if st.sidebar.checkbox("Show Moving Average Trendline"):
    ma_window = st.sidebar.slider("Select Moving Average Window (Years):", 5, 30, 10)
    yearly_temp['Moving_Average'] = yearly_temp['LandAverageTemperature'].rolling(window=ma_window).mean()
    fig.add_scatter(
        x=yearly_temp['Year'],
        y=yearly_temp['Moving_Average'],
        mode='lines',
        name=f'{ma_window}-Year Moving Average',
        line=dict(color='orange', dash='dash')
    )

# Display the chart
st.plotly_chart(fig, use_container_width=True)

# --- 8. Raw Data Display ---
with st.expander("📦 Click here to see the filtered raw data"):
    st.dataframe(filtered_df)
