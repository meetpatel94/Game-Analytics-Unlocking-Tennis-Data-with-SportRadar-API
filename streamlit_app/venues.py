import streamlit as st
import pandas as pd
import plotly.express as px
from queries.query import run_query

def show_venues():

    st.title("🏟 Venue Analytics")

    st.caption(
        "Analyze Tennis Venues, Cities, Countries and Complexes"
    )

    # =====================================
    # LOAD DATA
    # =====================================

    df = run_query("""
        SELECT
            v.venue_id,
            v.venue_name,
            v.city_name,
            v.country_name,
            v.country_code,
            v.timezone,
            c.complex_id,
            c.complex_name
        FROM venues v
        LEFT JOIN complexes c
        ON v.complex_id = c.complex_id
    """)

    # =====================================
    # KPI DATA
    # =====================================

    total_venues = len(df)

    total_complexes = (
        df["complex_name"]
        .nunique()
    )

    total_countries = (
        df["country_name"]
        .nunique()
    )

    total_cities = (
        df["city_name"]
        .nunique()
    )

    total_timezones = (
        df["timezone"]
        .nunique()
    )

    avg_venues_country = round(
        total_venues / max(total_countries, 1),
        2
    )

    # =====================================
    # KPI CARDS
    # =====================================

    k1, k2, k3 = st.columns(3)

    with k1:
        st.metric(
            "🏟 Total Venues",
            f"{total_venues:,}"
        )

    with k2:
        st.metric(
            "🏢 Complexes",
            f"{total_complexes:,}"
        )

    with k3:
        st.metric(
            "🌍 Countries",
            f"{total_countries:,}"
        )

    k4, k5, k6 = st.columns(3)

    with k4:
        st.metric(
            "🏙 Cities",
            f"{total_cities:,}"
        )

    with k5:
        st.metric(
            "🕒 Timezones",
            f"{total_timezones:,}"
        )

    with k6:
        st.metric(
            "📊 Avg Venues/Country",
            avg_venues_country
        )

    st.divider()

    # =====================================
    # FILTERS
    # =====================================

    st.subheader(
        "🎯 Venue Filters"
    )

    f1, f2 = st.columns(2)

    countries = sorted(
        df["country_name"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_country = f1.selectbox(
        "Country",
        ["All"] + countries
    )

    filtered_df = df.copy()

    if selected_country != "All":

        filtered_df = filtered_df[
            filtered_df["country_name"]
            == selected_country
        ]

    cities = sorted(
        filtered_df["city_name"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_city = f2.selectbox(
        "City",
        ["All"] + cities
    )

    if selected_city != "All":

        filtered_df = filtered_df[
            filtered_df["city_name"]
            == selected_city
        ]

    f3, f4 = st.columns(2)

    complexes = sorted(
        filtered_df["complex_name"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_complex = f3.selectbox(
        "Complex",
        ["All"] + complexes
    )

    if selected_complex != "All":

        filtered_df = filtered_df[
            filtered_df["complex_name"]
            == selected_complex
        ]

    timezones = sorted(
        filtered_df["timezone"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_timezone = f4.selectbox(
        "Timezone",
        ["All"] + timezones
    )

    if selected_timezone != "All":

        filtered_df = filtered_df[
            filtered_df["timezone"]
            == selected_timezone
        ]

    st.success(
        f"Showing {len(filtered_df):,} venues after applying filters."
    )

    st.divider()

    # =====================================
    # COUNTRY ANALYTICS
    # =====================================

    country_df = (
        filtered_df
        .groupby(
            ["country_name", "country_code"]
        )
        .size()
        .reset_index(name="total_venues")
        .sort_values(
            "total_venues",
            ascending=False
        )
    )

    city_df = (
        filtered_df
        .groupby("city_name")
        .size()
        .reset_index(name="total_venues")
        .sort_values(
            "total_venues",
            ascending=False
        )
        .head(15)
    )

    st.subheader(
        "🌍 Geographic Analytics"
    )

    geo1, geo2 = st.columns(2)

    with geo1:

        fig_country = px.bar(
            country_df.head(10),
            x="country_name",
            y="total_venues",
            text="total_venues",
            title="Top Venue Countries"
        )

        fig_country.update_layout(
            height=500
        )

        st.plotly_chart(
            fig_country,
            use_container_width=True
        )

    with geo2:

        fig_map = px.choropleth(
            country_df,
            locations="country_code",
            color="total_venues",
            hover_name="country_name",
            projection="natural earth",
            title="Global Venue Distribution"
        )

        fig_map.update_layout(
            height=500
        )

        st.plotly_chart(
            fig_map,
            use_container_width=True
        )

    st.divider()
        # =====================================
    # TOP CITIES
    # =====================================

    st.subheader(
        "🏙 City Analytics"
    )

    fig_city = px.bar(
        city_df,
        x="city_name",
        y="total_venues",
        text="total_venues",
        title="Top Cities by Venue Count"
    )

    fig_city.update_layout(
        height=500
    )

    st.plotly_chart(
        fig_city,
        use_container_width=True
    )

    st.divider()

    # =====================================
    # COMPLEX ANALYTICS
    # =====================================

    complex_df = (
        filtered_df
        .groupby("complex_name")
        .size()
        .reset_index(name="total_venues")
        .sort_values(
            "total_venues",
            ascending=False
        )
        .head(15)
    )

    st.subheader(
        "🏢 Complex Analytics"
    )

    fig_complex = px.bar(
        complex_df,
        x="complex_name",
        y="total_venues",
        text="total_venues",
        title="Top Complexes by Venue Count"
    )

    fig_complex.update_layout(
        height=550
    )

    st.plotly_chart(
        fig_complex,
        use_container_width=True
    )

    st.divider()

    # =====================================
    # TIMEZONE ANALYTICS
    # =====================================

    timezone_df = (
        filtered_df
        .groupby("timezone")
        .size()
        .reset_index(name="total_venues")
        .sort_values(
            "total_venues",
            ascending=False
        )
        .head(15)
    )

    st.subheader(
        "🕒 Timezone Analytics"
    )

    fig_timezone = px.bar(
        timezone_df,
        x="timezone",
        y="total_venues",
        text="total_venues",
        title="Venue Distribution by Timezone"
    )

    fig_timezone.update_layout(
        height=500
    )

    st.plotly_chart(
        fig_timezone,
        use_container_width=True
    )

    st.divider()

    # =====================================
    # GEOGRAPHIC INTELLIGENCE
    # =====================================

    st.subheader(
        "🌟 Geographic Intelligence"
    )

    top_country = (
        filtered_df["country_name"]
        .mode()
        .iloc[0]
        if len(filtered_df) > 0 else "-"
    )

    top_city = (
        filtered_df["city_name"]
        .mode()
        .iloc[0]
        if len(filtered_df) > 0 else "-"
    )

    top_complex = (
        filtered_df["complex_name"]
        .mode()
        .iloc[0]
        if len(filtered_df) > 0 else "-"
    )

    top_timezone = (
        filtered_df["timezone"]
        .mode()
        .iloc[0]
        if len(filtered_df) > 0 else "-"
    )

    g1, g2, g3, g4 = st.columns(4)

    with g1:
        st.metric(
            "🌍 Top Country",
            top_country
        )

    with g2:
        st.metric(
            "🏙 Top City",
            top_city
        )

    with g3:
        st.metric(
            "🏢 Top Complex",
            top_complex
        )

    with g4:
        st.metric(
            "🕒 Top Timezone",
            top_timezone
        )

    st.divider()

    # =====================================
    # VENUE EXPLORER
    # =====================================

    st.subheader(
        "🔍 Venue Explorer"
    )

    search_text = st.text_input(
        "Search Venue"
    )

    explorer_df = filtered_df.copy()

    if search_text:

        explorer_df = explorer_df[
            explorer_df["venue_name"]
            .str.contains(
                search_text,
                case=False,
                na=False
            )
        ]

    st.dataframe(
        explorer_df[
            [
                "venue_name",
                "city_name",
                "country_name",
                "complex_name",
                "timezone"
            ]
        ],
        use_container_width=True,
        hide_index=True,
        height=500
    )

    st.divider()

    # =====================================
    # EXPORT DATA
    # =====================================

    st.subheader(
        "📥 Export Data"
    )

    csv = explorer_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="📥 Download Filtered Venues",
        data=csv,
        file_name="filtered_venues.csv",
        mime="text/csv"
    )