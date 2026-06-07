import streamlit as st
import pandas as pd
import plotly.express as px

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(
    page_title="Web Traffic Analytics Dashboard",
    page_icon="🌐",
    layout="wide"
)

# ==============================
# LOAD DATA
# ==============================
@st.cache_data
def load_data():
    df = pd.read_csv("data/website_wata.csv")

    # Remove extra spaces from column names
    df.columns = df.columns.str.strip()

    return df

df = load_data()

# ==============================
# HEADER
# ==============================
st.title("🌐 Web Traffic Analytics Dashboard")
st.markdown("Analyze Website Performance and User Behavior")

# ==============================
# SIDEBAR FILTER
# ==============================
st.sidebar.header("Filters")

sources = st.sidebar.multiselect(
    "Traffic Source",
    options=df["Traffic Source"].unique(),
    default=df["Traffic Source"].unique()
)

filtered_df = df[
    df["Traffic Source"].isin(sources)
]

# ==============================
# KPI SECTION
# ==============================
total_views = filtered_df["Page Views"].sum()

avg_session = filtered_df["Session Duration"].mean()

avg_bounce = filtered_df["Bounce Rate"].mean()

avg_conversion = filtered_df["Conversion Rate"].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "👁 Page Views",
    f"{total_views:,.0f}"
)

col2.metric(
    "⏱ Avg Session",
    f"{avg_session:.2f} min"
)

col3.metric(
    "🚪 Bounce Rate",
    f"{avg_bounce:.2f}%"
)

col4.metric(
    "🎯 Conversion Rate",
    f"{avg_conversion:.2f}%"
)

st.divider()

# ==============================
# TRAFFIC SOURCE ANALYSIS
# ==============================
col1, col2 = st.columns(2)

with col1:

    source_views = (
        filtered_df.groupby("Traffic Source")["Page Views"]
        .sum()
        .reset_index()
    )

    fig1 = px.bar(
        source_views,
        x="Traffic Source",
        y="Page Views",
        title="Traffic Source vs Page Views",
        text_auto=True
    )

    st.plotly_chart(fig1, use_container_width=True)

with col2:

    source_conversion = (
        filtered_df.groupby("Traffic Source")["Conversion Rate"]
        .mean()
        .reset_index()
    )

    fig2 = px.pie(
        source_conversion,
        names="Traffic Source",
        values="Conversion Rate",
        hole=0.4,
        title="Conversion Rate by Traffic Source"
    )

    st.plotly_chart(fig2, use_container_width=True)

# ==============================
# SESSION DURATION
# ==============================
st.subheader("⏱ Session Duration Distribution")

fig3 = px.histogram(
    filtered_df,
    x="Session Duration",
    nbins=20,
    title="Session Duration"
)

st.plotly_chart(fig3, use_container_width=True)

# ==============================
# BOUNCE RATE ANALYSIS
# ==============================
st.subheader("🚪 Bounce Rate Analysis")

bounce = (
    filtered_df.groupby("Traffic Source")["Bounce Rate"]
    .mean()
    .reset_index()
)

fig4 = px.bar(
    bounce,
    x="Traffic Source",
    y="Bounce Rate",
    color="Traffic Source",
    title="Average Bounce Rate"
)

st.plotly_chart(fig4, use_container_width=True)

# ==============================
# TIME ON PAGE
# ==============================
st.subheader("📄 Time on Page")

fig5 = px.box(
    filtered_df,
    x="Traffic Source",
    y="Time on Page",
    color="Traffic Source",
    title="Time Spent on Page"
)

st.plotly_chart(fig5, use_container_width=True)

# ==============================
# PREVIOUS VISITS
# ==============================
st.subheader("🔁 Previous Visits vs Conversion Rate")

fig6 = px.scatter(
    filtered_df,
    x="Previous Visits",
    y="Conversion Rate",
    color="Traffic Source",
    title="Returning Visitors vs Conversion"
)

st.plotly_chart(fig6, use_container_width=True)

# ==============================
# CORRELATION MATRIX
# ==============================
st.subheader("📊 Correlation Matrix")

corr = filtered_df[
    [
        "Page Views",
        "Session Duration",
        "Bounce Rate",
        "Time on Page",
        "Previous Visits",
        "Conversion Rate"
    ]
].corr()

fig7 = px.imshow(
    corr,
    text_auto=True,
    aspect="auto",
    title="Feature Correlation"
)

st.plotly_chart(fig7, use_container_width=True)

# ==============================
# INSIGHTS
# ==============================
st.subheader("🤖 Business Insights")

best_source = (
    filtered_df.groupby("Traffic Source")["Conversion Rate"]
    .mean()
    .idxmax()
)

worst_source = (
    filtered_df.groupby("Traffic Source")["Bounce Rate"]
    .mean()
    .idxmax()
)

st.success(
    f"Highest Conversion Rate Source: {best_source}"
)

st.warning(
    f"Highest Bounce Rate Source: {worst_source}"
)

st.info(
    "Users with more previous visits generally have a higher chance of conversion."
)

# ==============================
# DATA PREVIEW
# ==============================
with st.expander("View Dataset"):

    st.dataframe(filtered_df.head(20))

# ==============================
# FOOTER
# ==============================
st.markdown("---")
st.caption("Developed by Ananya Kumari")