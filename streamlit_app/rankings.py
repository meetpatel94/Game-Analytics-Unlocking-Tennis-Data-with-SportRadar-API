import streamlit as st
import pandas as pd
import plotly.express as px

from queries.query import run_query

# =============================CSS==============
# ==============================================
st.markdown("""
    <style>
    
    </style>
""", unsafe_allow_html=True)
# =============================CSS=============
# =============================================

def show_rankings():

    st.title("📈 Rankings Analytics")

    st.caption(
        "Analyze Rankings, Points, Movement and Player Performance"
    )

    # =====================================
    # LOAD DATA
    # =====================================

    df = run_query("""
        SELECT
            r.competitor_id,
            r.rank,
            r.points,
            r.movement,
            r.competitions_played,
            r.ranking_type,
            c.competitor_name,
            c.country,
            c.country_code,
            c.abbreviation
        FROM competitor_rankings r
        JOIN competitors c
        ON r.competitor_id = c.competitor_id
    """)

    # =====================================
    # KPI DATA
    # =====================================

    total_rankings = len(df)

    highest_points = int(
        df["points"].max()
    )

    avg_points = round(
        df["points"].mean(),
        2
    )

    top_ranked_players = len(
        df[
            df["rank"] <= 10
        ]
    )

    avg_movement = round(
        df["movement"].mean(),
        2
    )

    avg_competitions = round(
        df["competitions_played"].mean(),
        2
    )

    # =====================================
    # KPI CARDS
    # =====================================

    k1, k2, k3 = st.columns(3)

    with k1:
        st.metric(
            "📈 Total Rankings",
            f"{total_rankings:,}"
        )

    with k2:
        st.metric(
            "🔥 Highest Points",
            f"{highest_points:,}"
        )

    with k3:
        st.metric(
            "📊 Average Points",
            avg_points
        )

    k4, k5, k6 = st.columns(3)

    with k4:
        st.metric(
            "🏆 Top 10 Players",
            top_ranked_players
        )

    with k5:
        st.metric(
            "🚀 Avg Movement",
            avg_movement
        )

    with k6:
        st.metric(
            "🎾 Avg Competitions",
            avg_competitions
        )

    st.divider()

    # =====================================
    # FILTERS
    # =====================================

    st.subheader(
        "🎯 Ranking Filters"
    )

    f1, f2, f3 = st.columns(3)

    ranking_types = sorted(
        df["ranking_type"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_ranking = f1.selectbox(
        "Ranking Type",
        ["All"] + ranking_types
    )

    filtered_df = df.copy()

    if selected_ranking != "All":

        filtered_df = filtered_df[
            filtered_df["ranking_type"]
            == selected_ranking
        ]

    countries = sorted(
        filtered_df["country"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_country = f2.selectbox(
        "Country",
        ["All"] + countries
    )

    if selected_country != "All":

        filtered_df = filtered_df[
            filtered_df["country"]
            == selected_country
        ]

    point_range = f3.selectbox(
        "Points Range",
        [
            "All",
            "0 - 1000",
            "1001 - 3000",
            "3001 - 5000",
            "5001+"
        ]
    )

    if point_range == "0 - 1000":

        filtered_df = filtered_df[
            filtered_df["points"] <= 1000
        ]

    elif point_range == "1001 - 3000":

        filtered_df = filtered_df[
            (filtered_df["points"] >= 1001)
            &
            (filtered_df["points"] <= 3000)
        ]

    elif point_range == "3001 - 5000":

        filtered_df = filtered_df[
            (filtered_df["points"] >= 3001)
            &
            (filtered_df["points"] <= 5000)
        ]

    elif point_range == "5001+":

        filtered_df = filtered_df[
            filtered_df["points"] > 5000
        ]

    st.success(
        f"Showing {len(filtered_df):,} rankings after applying filters."
    )

    st.divider()
        # =====================================
    # RANKING DISTRIBUTION
    # =====================================

    st.subheader(
        "📊 Ranking Distribution Analytics"
    )

    r1, r2 = st.columns(2)

    with r1:

        fig_rank_dist = px.histogram(
            filtered_df,
            x="rank",
            nbins=40,
            title="Ranking Distribution"
        )

        fig_rank_dist.update_layout(
            height=450
        )

        st.plotly_chart(
            fig_rank_dist,
            use_container_width=True
        )

    with r2:

        fig_points_dist = px.histogram(
            filtered_df,
            x="points",
            nbins=40,
            title="Points Distribution"
        )

        fig_points_dist.update_layout(
            height=450
        )

        st.plotly_chart(
            fig_points_dist,
            use_container_width=True
        )

    st.divider()

    # =====================================
    # COUNTRY RANKING ANALYTICS
    # =====================================

    ranked_country_df = (
        filtered_df
        .groupby("country")
        .size()
        .reset_index(name="total_players")
        .sort_values(
            "total_players",
            ascending=False
        )
        .head(15)
    )

    avg_points_country_df = (
        filtered_df
        .groupby("country")
        .agg(
            avg_points=("points", "mean"),
            total_players=("competitor_id", "count")
        )
        .reset_index()
    )

    avg_points_country_df = (
        avg_points_country_df[
            avg_points_country_df["total_players"] >= 3
        ]
        .sort_values(
            "avg_points",
            ascending=False
        )
        .head(15)
    )

    st.subheader(
        "🌍 Country Ranking Analytics"
    )

    c1, c2 = st.columns(2)

    with c1:

        fig_ranked_country = px.bar(
            ranked_country_df,
            x="country",
            y="total_players",
            text="total_players",
            title="Top Countries by Ranked Players"
        )

        fig_ranked_country.update_layout(
            height=500
        )

        st.plotly_chart(
            fig_ranked_country,
            use_container_width=True
        )

    with c2:

        fig_avg_points = px.bar(
            avg_points_country_df,
            x="country",
            y="avg_points",
            text="avg_points",
            title="Top Countries by Average Points"
        )

        fig_avg_points.update_layout(
            height=500
        )

        st.plotly_chart(
            fig_avg_points,
            use_container_width=True
        )

    st.divider()

    # =====================================
    # ELITE PLAYERS ANALYSIS
    # =====================================

    st.subheader(
        "🥇 Elite Players Analysis"
    )

    elite_filter = st.selectbox(
        "Select Ranking Tier",
        [
            "Top 10",
            "Top 50",
            "Top 100",
            "Top 250"
        ]
    )

    if elite_filter == "Top 10":

        elite_df = filtered_df[
            filtered_df["rank"] <= 10
        ]

    elif elite_filter == "Top 50":

        elite_df = filtered_df[
            filtered_df["rank"] <= 50
        ]

    elif elite_filter == "Top 100":

        elite_df = filtered_df[
            filtered_df["rank"] <= 100
        ]

    else:

        elite_df = filtered_df[
            filtered_df["rank"] <= 250
        ]

    st.dataframe(
        elite_df[
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
        height=400
    )

    st.divider()

    # =====================================
    # POINTS VS RANK ANALYSIS
    # =====================================

    st.subheader(
        "📈 Points vs Rank Analysis"
    )

    scatter_df = (
        filtered_df
        .sort_values("rank")
        .head(300)
    )

    fig_scatter = px.scatter(
        scatter_df,
        x="rank",
        y="points",
        hover_name="competitor_name",
        hover_data=[
            "country",
            "movement"
        ],
        title="Points vs Rank Scatter Plot"
    )

    fig_scatter.update_layout(
        height=550
    )

    st.plotly_chart(
        fig_scatter,
        use_container_width=True
    )

    st.divider()
        # =====================================
    # TOP GAINERS
    # =====================================

    gainers_df = (
        filtered_df
        .sort_values(
            "movement",
            ascending=False
        )
        .head(10)
    )

    # =====================================
    # TOP LOSERS
    # =====================================

    losers_df = (
        filtered_df
        .sort_values(
            "movement",
            ascending=True
        )
        .head(10)
    )

    st.subheader(
        "🚀 Ranking Movement Intelligence"
    )

    g1, g2 = st.columns(2)

    with g1:

        st.success(
            "Top Gainers"
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

    with g2:

        st.error(
            "Top Losers"
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
    # RANKING TIERS
    # =====================================

    st.subheader(
        "🏆 Ranking Tiers Analysis"
    )

    tier_df = filtered_df.copy()

    def get_tier(rank):

        if rank <= 10:
            return "Elite (1-10)"

        elif rank <= 50:
            return "Professional (11-50)"

        elif rank <= 100:
            return "Advanced (51-100)"

        else:
            return "Competitive (101+)"

    tier_df["tier"] = tier_df[
        "rank"
    ].apply(get_tier)

    tier_summary = (
        tier_df
        .groupby("tier")
        .size()
        .reset_index(name="players")
    )

    fig_tier = px.pie(
        tier_summary,
        names="tier",
        values="players",
        hole=0.5,
        title="Ranking Tier Distribution"
    )

    fig_tier.update_layout(
        height=500
    )

    st.plotly_chart(
        fig_tier,
        use_container_width=True
    )

    st.divider()

    # =====================================
    # RANKING EXPLORER
    # =====================================

    st.subheader(
        "🔍 Ranking Explorer"
    )

    search_player = st.text_input(
        "Search Ranked Player"
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
                "rank",
                "competitor_name",
                "country",
                "points",
                "movement",
                "competitions_played",
                "ranking_type"
            ]
        ],
        use_container_width=True,
        hide_index=True,
        height=500
    )

    st.divider()

    # =====================================
    # PLAYER RANKING PROFILE
    # =====================================

    st.subheader(
        "👤 Ranking Profile"
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
                    "Ranking Type",
                    player["ranking_type"]
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
        label="📥 Download Filtered Rankings",
        data=csv,
        file_name="filtered_rankings.csv",
        mime="text/csv"
    )