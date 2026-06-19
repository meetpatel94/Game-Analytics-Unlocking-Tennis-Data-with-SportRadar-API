import streamlit as st
import plotly.express as px

from queries.query import run_query

def show_competitions():

    st.title("🏆 Competitions Analytics")

    st.caption(
        "Analyze Tennis Competitions, Categories, Types and Levels"
    )

    # =====================================
    # LOAD DATA (ONLY ONE QUERY)
    # =====================================

    df = run_query("""
    SELECT
        cp.competition_id,
        cp.competition_name,
        cp.parent_id,
        cp.type,
        cp.gender,
        cp.category_id,
        c.category_name
    FROM competitions cp
    LEFT JOIN categories c
    ON cp.category_id = c.category_id
    """)

    # =====================================
    # KPI CALCULATIONS
    # =====================================

    total_competitions = len(df)

    total_categories = (
        df["category_name"]
        .nunique()
    )

    singles_count = len(
        df[
            df["type"]
            .str.lower()
            == "singles"
        ]
    )

    doubles_count = len(
        df[
            df["type"]
            .str.lower()
            == "doubles"
        ]
    )

    mixed_count = len(
        df[
            df["gender"]
            .str.lower()
            == "mixed"
        ]
    )

    men_count = len(
        df[
            df["gender"]
            .str.lower()
            == "men"
        ]
    )

    # =====================================
    # KPI CARDS
    # =====================================

    k1, k2, k3 = st.columns(3)

    with k1:
        st.metric(
            "🏆 Competitions",
            f"{total_competitions:,}"
        )

    with k2:
        st.metric(
            "📂 Categories",
            total_categories
        )

    with k3:
        st.metric(
            "👨 Men's Events",
            f"{men_count:,}"
        )

    k4, k5, k6 = st.columns(3)

    with k4:
        st.metric(
            "🎾 Singles",
            f"{singles_count:,}"
        )

    with k5:
        st.metric(
            "👥 Doubles",
            f"{doubles_count:,}"
        )

    with k6:
        st.metric(
            "🤝 Mixed",
            f"{mixed_count:,}"
        )

    st.divider()
        # =====================================
    # FILTERS
    # =====================================

    st.subheader("🎯 Competition Filters")

    f1, f2, f3 = st.columns(3)

    categories = sorted(
        df["category_name"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_category = f1.selectbox(
        "Category",
        ["All"] + categories
    )

    selected_gender = f2.selectbox(
        "Gender",
        ["All"] + sorted(
            df["gender"]
            .dropna()
            .unique()
            .tolist()
        )
    )

    selected_type = f3.selectbox(
        "Type",
        ["All"] + sorted(
            df["type"]
            .dropna()
            .unique()
            .tolist()
        )
    )

    filtered_df = df.copy()

    if selected_category != "All":
        filtered_df = filtered_df[
            filtered_df["category_name"]
            == selected_category
        ]

    if selected_gender != "All":
        filtered_df = filtered_df[
            filtered_df["gender"]
            == selected_gender
        ]

    if selected_type != "All":
        filtered_df = filtered_df[
            filtered_df["type"]
            == selected_type
        ]

    st.success(
        f"Showing {len(filtered_df):,} competitions"
    )

    st.divider()

    # =====================================
    # CHART DATA
    # =====================================

    category_chart = (
        filtered_df
        .groupby("category_name")
        .size()
        .reset_index(name="total")
        .sort_values(
            "total",
            ascending=False
        )
        .head(10)
    )

    gender_chart = (
        filtered_df
        .groupby("gender")
        .size()
        .reset_index(name="total")
    )

    type_chart = (
        filtered_df
        .groupby("type")
        .size()
        .reset_index(name="total")
    )

    # =====================================
    # ANALYTICS CHARTS
    # =====================================

    st.subheader("📊 Competition Analytics")

    c1, c2 = st.columns(2)

    with c1:

        fig_category = px.bar(
            category_chart,
            x="category_name",
            y="total",
            text="total",
            title="Top Categories"
        )

        fig_category.update_layout(
            height=450
        )

        st.plotly_chart(
            fig_category,
            use_container_width=True
        )

    with c2:

        fig_gender = px.pie(
            gender_chart,
            names="gender",
            values="total",
            hole=0.5,
            title="Gender Distribution"
        )

        fig_gender.update_layout(
            height=450
        )

        st.plotly_chart(
            fig_gender,
            use_container_width=True
        )

    st.divider()

    # =====================================
    # TYPE ANALYTICS
    # =====================================

    st.subheader("🏆 Competition Types")

    fig_type = px.bar(
        type_chart,
        x="type",
        y="total",
        text="total",
        color="type"
    )

    fig_type.update_layout(
        height=500
    )

    st.plotly_chart(
        fig_type,
        use_container_width=True
    )

    st.divider()
        # =====================================
    # COMPETITION EXPLORER
    # =====================================

    st.subheader("🔍 Competition Explorer")

    search_text = st.text_input(
        "Search Competition Name"
    )

    explorer_df = filtered_df.copy()

    if search_text:

        explorer_df = explorer_df[
            explorer_df["competition_name"]
            .str.contains(
                search_text,
                case=False,
                na=False
            )
        ]

    st.dataframe(
        explorer_df[
            [
                "competition_name",
                "category_name",
                "gender",
                "type"
            ]
        ],
        use_container_width=True,
        hide_index=True,
        height=500
    )

    st.divider()

    # =====================================
    # TOP CATEGORIES
    # =====================================

    st.subheader("🏅 Top Categories")

    top_categories = (
        filtered_df
        .groupby("category_name")
        .size()
        .reset_index(name="competitions")
        .sort_values(
            "competitions",
            ascending=False
        )
        .head(15)
    )

    fig_top = px.bar(
        top_categories,
        x="competitions",
        y="category_name",
        orientation="h",
        text="competitions"
    )

    fig_top.update_layout(
        height=600,
        yaxis={
            "categoryorder":
            "total ascending"
        }
    )

    st.plotly_chart(
        fig_top,
        use_container_width=True
    )

    st.divider()

    # =====================================
    # INSIGHTS
    # =====================================

    st.subheader("🎯 Competition Insights")

    if len(filtered_df) > 0:

        top_category = (
            filtered_df["category_name"]
            .mode()
            .iloc[0]
        )

        top_type = (
            filtered_df["type"]
            .mode()
            .iloc[0]
        )

        top_gender = (
            filtered_df["gender"]
            .mode()
            .iloc[0]
        )

        st.info(
            f"""
• Most active category: **{top_category}**

• Most common type: **{top_type}**

• Most common gender: **{top_gender}**

• Filtered competitions: **{len(filtered_df):,}**
"""
        )

    st.divider()

    # =====================================
    # DOWNLOAD
    # =====================================

    csv = explorer_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        "📥 Download Data",
        data=csv,
        file_name="competitions.csv",
        mime="text/csv"
    )