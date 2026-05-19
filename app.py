import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ======================
# PAGE CONFIG
# ======================

st.set_page_config(
    page_title="Restaurant Analytics Dashboard",
    page_icon="🍽️",
    layout="wide"
)

# ======================
# LOAD DATA
# ======================

df = pd.read_csv("Dataset.csv")

# ======================
# SIDEBAR
# ======================

st.sidebar.title("Dashboard Filters")

# Country Filter
country = st.sidebar.selectbox(
    "Select Country",
    sorted(df['Country Code'].dropna().unique())
)

filtered_df = df[df['Country Code'] == country]

# City Filter
city = st.sidebar.selectbox(
    "Select City",
    sorted(filtered_df['City'].dropna().unique())
)

filtered_df = filtered_df[
    filtered_df['City'] == city
]

# Online Delivery Filter
delivery_filter = st.sidebar.selectbox(
    "Online Delivery",
    ["All", "Yes", "No"]
)

if delivery_filter != "All":
    filtered_df = filtered_df[
        filtered_df['Has Online delivery'] == delivery_filter
    ]

# Table Booking Filter
booking_filter = st.sidebar.selectbox(
    "Table Booking",
    ["All", "Yes", "No"]
)

if booking_filter != "All":
    filtered_df = filtered_df[
        filtered_df['Has Table booking'] == booking_filter
    ]

# ======================
# TITLE
# ======================

st.title("🍽️ Restaurant Data Analysis Dashboard")

st.markdown("""
Interactive analytics dashboard built using Streamlit, Python, Pandas, and Matplotlib.
""")

# ======================
# KPI SECTION
# ======================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Restaurants",
    filtered_df.shape[0]
)

col2.metric(
    "Average Rating",
    round(filtered_df['Aggregate rating'].mean(), 2)
)

col3.metric(
    "Average Cost for Two",
    round(filtered_df['Average Cost for two'].mean(), 2)
)

col4.metric(
    "Total Votes",
    int(filtered_df['Votes'].sum())
)

# ======================
# TABS
# ======================

tab1, tab2, tab3 = st.tabs([
    "Overview",
    "Visual Analytics",
    "Dataset"
])

# ======================
# OVERVIEW TAB
# ======================

with tab1:

    st.header("Business Insights")

    st.info(f"""
    Selected Country: {country}
    
    Selected City: {city}
    """)

    st.success("""
    This dashboard helps analyze restaurant trends, customer preferences,
    pricing, ratings, delivery availability, and booking patterns.
    """)

    st.subheader("Top Rated Restaurants")

    top_restaurants = filtered_df[
        ['Restaurant Name', 'Aggregate rating', 'Votes']
    ].sort_values(
        by='Aggregate rating',
        ascending=False
    ).head(10)

    st.dataframe(top_restaurants)

# ======================
# VISUAL ANALYTICS TAB
# ======================

with tab2:

    colA, colB = st.columns(2)

    # ----------------------
    # Top Cuisines
    # ----------------------

    with colA:

        st.subheader("Top 10 Cuisines")

        top_cuisines = (
            filtered_df['Cuisines']
            .value_counts()
            .head(10)
        )

        fig1, ax1 = plt.subplots()

        top_cuisines.plot(
            kind='barh',
            ax=ax1
        )

        st.pyplot(fig1)

    # ----------------------
    # Online Delivery
    # ----------------------

    with colB:

        st.subheader("Online Delivery Availability")

        delivery_counts = (
            filtered_df['Has Online delivery']
            .value_counts()
        )

        fig2, ax2 = plt.subplots()

        delivery_counts.plot(
            kind='pie',
            autopct='%1.1f%%',
            ax=ax2
        )

        st.pyplot(fig2)

    # ----------------------
    # Price Range
    # ----------------------

    colC, colD = st.columns(2)

    with colC:

        st.subheader("Price Range Distribution")

        fig3, ax3 = plt.subplots()

        filtered_df['Price range'].value_counts().sort_index().plot(
            kind='bar',
            ax=ax3
        )

        st.pyplot(fig3)

    # ----------------------
    # Ratings Distribution
    # ----------------------

    with colD:

        st.subheader("Ratings Distribution")

        fig4, ax4 = plt.subplots()

        filtered_df['Aggregate rating'].plot(
            kind='hist',
            bins=10,
            ax=ax4
        )

        st.pyplot(fig4)

    # ----------------------
    # Votes vs Ratings
    # ----------------------

    st.subheader("Votes vs Ratings")

    fig5, ax5 = plt.subplots()

    ax5.scatter(
        filtered_df['Votes'],
        filtered_df['Aggregate rating']
    )

    ax5.set_xlabel("Votes")
    ax5.set_ylabel("Aggregate Rating")

    st.pyplot(fig5)

# ======================
# DATASET TAB
# ======================

with tab3:

    st.subheader("Dataset Preview")

    st.dataframe(filtered_df)

    st.subheader("Dataset Shape")

    st.write(filtered_df.shape)

    st.subheader("Columns")

    st.write(filtered_df.columns.tolist())

# ======================
# FOOTER
# ======================

st.markdown("---")

st.markdown("""
Created by Devanshi Baraskar using Streamlit and Python
""")