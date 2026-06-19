import streamlit as st
import pandas as pd
import plotly.express as px

from queries.query import run_query


def show_competitors():

    st.title("👤 Competitor Analytics")

    st.caption(
        "Analyze Tennis Players, Rankings and Country Performance"
    )

    # =====================================
    # LOAD DATA
    # =====================================

    df = run_query("""
        SELECT
            c.competitor_id,
            c.competitor_name,
            c.country,
            c.country_code,
            c.abbreviation,
            r.rank,
            r.points,
            r.movement,
            r.competitions_played,
            r.ranking_type
        FROM competitors c
        LEFT JOIN competitor_rankings r
        ON c.competitor_id = r.competitor_id
    """)

    # =====================================
    # KPI DATA
    # =====================================

    total_competitors = (
        df["competitor_id"]
        .nunique()
    )

    total_countries = (
        df["country"]
        .nunique()
    )

    top_ranked_players = len(
        df[
            df["rank"] <= 10
        ]
    )

    avg_points = round(
        df["points"].mean(),
        2
    )

    avg_competitions = round(
        df["competitions_played"].mean(),
        2
    )

    active_players = len(
        df[
            df["points"] > 0
        ]
    )

    # =====================================
    # KPI CARDS
    # =====================================

    k1, k2, k3 = st.columns(3)

    with k1:
        st.metric(
            "👤 Competitors",
            f"{total_competitors:,}"
        )

    with k2:
        st.metric(
            "🌍 Countries",
            f"{total_countries:,}"
        )

    with k3:
        st.metric(
            "🏆 Top 10 Players",
            f"{top_ranked_players:,}"
        )

    k4, k5, k6 = st.columns(3)

    with k4:
        st.metric(
            "🎾 Active Players",
            f"{active_players:,}"
        )

    with k5:
        st.metric(
            "📈 Avg Points",
            avg_points
        )

    with k6:
        st.metric(
            "🏟 Avg Competitions",
            avg_competitions
        )

    st.divider()

    # =====================================
    # FILTERS
    # =====================================

    st.subheader(
        "🎯 Player Filters"
    )

    f1, f2 = st.columns(2)

    countries = sorted(
        df["country"]
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
            filtered_df["country"]
            == selected_country
        ]

    ranking_types = sorted(
        filtered_df["ranking_type"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_ranking = f2.selectbox(
        "Ranking Type",
        ["All"] + ranking_types
    )

    if selected_ranking != "All":

        filtered_df = filtered_df[
            filtered_df["ranking_type"]
            == selected_ranking
        ]

    st.success(
        f"Showing {len(filtered_df):,} players after applying filters."
    )

    st.divider()
        # =====================================
    # TOP PLAYER COUNTRIES
    # =====================================

    country_players_df = (
        filtered_df
        .groupby("country")
        .size()
        .reset_index(name="total_players")
        .sort_values(
            "total_players",
            ascending=False
        )
        .head(10)
    )

    # =====================================
    # COUNTRY REPRESENTATION
    # =====================================

    country_representation_df = (
        filtered_df
        .groupby("country")
        .size()
        .reset_index(name="players")
        .sort_values(
            "players",
            ascending=False
        )
        .head(10)
    )

    st.subheader(
        "🌍 Country Analytics"
    )

    c1, c2 = st.columns(2)

    with c1:

        fig_country = px.bar(
            country_players_df,
            x="country",
            y="total_players",
            text="total_players",
            title="Top Player Countries"
        )

        fig_country.update_layout(
            height=450
        )

        st.plotly_chart(
            fig_country,
            use_container_width=True
        )

    with c2:

        fig_representation = px.pie(
            country_representation_df,
            names="country",
            values="players",
            hole=0.5,
            title="Country Representation"
        )

        fig_representation.update_layout(
            height=450
        )

        st.plotly_chart(
            fig_representation,
            use_container_width=True
        )

    st.divider()

    # =====================================
    # COUNTRY RANKING STRENGTH
    # =====================================

    country_strength_df = (
        filtered_df
        .groupby("country")
        .agg(
            avg_points=("points", "mean"),
            total_players=("competitor_id", "count")
        )
        .reset_index()
    )

    country_strength_df = (
        country_strength_df[
            country_strength_df["total_players"] >= 3
        ]
        .sort_values(
            "avg_points",
            ascending=False
        )
        .head(15)
    )

    st.subheader(
        "🏆 Country Ranking Strength"
    )

    fig_strength = px.bar(
        country_strength_df,
        x="country",
        y="avg_points",
        text="avg_points"
    )

    fig_strength.update_layout(
        height=500
    )

    st.plotly_chart(
        fig_strength,
        use_container_width=True
    )

    st.divider()

    # =====================================
    # TOP 10 PLAYERS
    # =====================================

    st.subheader(
        "🥇 Top Ranked Players"
    )

    leaderboard_df = (
        filtered_df
        .sort_values("rank")
        .head(10)
    )

    st.dataframe(
        leaderboard_df[
            [
                "rank",
                "competitor_name",
                "country",
                "points",
                "movement",
                "competitions_played"
            ]
        ],
        use_container_width=True,
        hide_index=True,
        height=420
    )

    st.divider()
        # =====================================
    # TOP GAINERS / LOSERS
    # =====================================

    movement_df = filtered_df.copy()

    gainers_df = (
        movement_df
        .sort_values(
            "movement",
            ascending=False
        )
        .head(10)
    )

    losers_df = (
        movement_df
        .sort_values(
            "movement",
            ascending=True
        )
        .head(10)
    )

    st.subheader(
        "📈 Ranking Movement Analysis"
    )

    m1, m2 = st.columns(2)

    with m1:

        st.success(
            "🚀 Top Gainers"
        )

        st.dataframe(
            gainers_df[
                [
                    "competitor_name",
                    "country",
                    "rank",
                    "movement",
                    "points"
                ]
            ],
            use_container_width=True,
            hide_index=True,
            height=350
        )

    with m2:

        st.error(
            "📉 Top Losers"
        )

        st.dataframe(
            losers_df[
                [
                    "competitor_name",
                    "country",
                    "rank",
                    "movement",
                    "points"
                ]
            ],
            use_container_width=True,
            hide_index=True,
            height=350
        )

    st.divider()

    # =====================================
    # COUNTRY INTELLIGENCE
    # =====================================

    st.subheader(
        "🌟 Country Intelligence"
    )

    top_country = (
        filtered_df["country"]
        .mode()
        .iloc[0]
        if len(filtered_df) > 0 else "-"
    )

    strongest_country = (
        country_strength_df.iloc[0]["country"]
        if len(country_strength_df) > 0
        else "-"
    )

    best_rank_country = (
        filtered_df
        .sort_values("rank")
        .iloc[0]["country"]
        if len(filtered_df) > 0
        else "-"
    )

    active_country = (
        filtered_df
        .groupby("country")
        .size()
        .reset_index(name="players")
        .sort_values(
            "players",
            ascending=False
        )
        .iloc[0]["country"]
        if len(filtered_df) > 0
        else "-"
    )

    ci1, ci2, ci3, ci4 = st.columns(4)

    with ci1:
        st.metric(
            "🌍 Most Represented",
            top_country
        )

    with ci2:
        st.metric(
            "🏆 Strongest Country",
            strongest_country
        )

    with ci3:
        st.metric(
            "🥇 Best Ranked Country",
            best_rank_country
        )

    with ci4:
        st.metric(
            "🎾 Most Active Country",
            active_country
        )

    st.divider()

    # =====================================
    # PLAYER EXPLORER
    # =====================================

    st.subheader(
        "🔍 Player Explorer"
    )

    search_player = st.text_input(
        "Search Player"
    )

    explorer_df = filtered_df.copy()

    if search_player:

        explorer_df = explorer_df[
            explorer_df["competitor_name"]
            .str.contains(
                search_player,
                case=False,
                na=False
            )
        ]

    st.dataframe(
        explorer_df[
            [
                "competitor_name",
                "country",
                "rank",
                "points",
                "movement",
                "competitions_played"
            ]
        ],
        use_container_width=True,
        hide_index=True,
        height=450
    )

    st.divider()

    # =====================================
    # PLAYER PROFILE
    # =====================================

    st.subheader(
        "👤 Player Profile"
    )

    player_list = sorted(
        explorer_df["competitor_name"]
        .dropna()
        .unique()
        .tolist()
    )

    if len(player_list) > 0:

        selected_player = st.selectbox(
            "Select Player",
            player_list
        )

        player_df = explorer_df[
            explorer_df["competitor_name"]
            == selected_player
        ]

        if len(player_df) > 0:

            player = player_df.iloc[0]

            p1, p2, p3 = st.columns(3)

            with p1:
                st.metric(
                    "Country",
                    player["country"]
                )

            with p2:
                st.metric(
                    "Rank",
                    f"#{player['rank']}"
                )

            with p3:
                st.metric(
                    "Points",
                    f"{player['points']:,}"
                )

            p4, p5, p6 = st.columns(3)

            with p4:
                st.metric(
                    "Movement",
                    player["movement"]
                )

            with p5:
                st.metric(
                    "Competitions",
                    player["competitions_played"]
                )

            with p6:
                st.metric(
                    "Abbreviation",
                    player["abbreviation"]
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
        label="📥 Download Filtered Players",
        data=csv,
        file_name="filtered_players.csv",
        mime="text/csv"
    )