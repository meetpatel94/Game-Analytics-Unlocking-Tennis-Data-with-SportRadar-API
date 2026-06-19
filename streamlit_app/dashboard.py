import streamlit as st
import plotly.express as px

from queries.query import run_query

def show_dashboard():

    st.title("🎾 Tennis Analytics Dashboard")
    st.caption("SportRadar Tennis Intelligence Platform")

    # =====================================
    # SINGLE KPI QUERY
    # =====================================

    kpi_df = run_query("""
    SELECT
        (SELECT COUNT(*) FROM categories) AS categories,
        (SELECT COUNT(*) FROM competitions) AS competitions,
        (SELECT COUNT(*) FROM complexes) AS complexes,
        (SELECT COUNT(*) FROM venues) AS venues,
        (SELECT COUNT(*) FROM competitors) AS competitors,
        (SELECT COUNT(*) FROM competitor_rankings) AS rankings
    """)

    total_categories = int(kpi_df.iloc[0]["categories"])
    total_competitions = int(kpi_df.iloc[0]["competitions"])
    total_complexes = int(kpi_df.iloc[0]["complexes"])
    total_venues = int(kpi_df.iloc[0]["venues"])
    total_competitors = int(kpi_df.iloc[0]["competitors"])
    total_rankings = int(kpi_df.iloc[0]["rankings"])

    # =====================================
    # KPI CARDS
    # =====================================

    st.subheader("📊 Platform Overview")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "🏆 Competitions",
            f"{total_competitions:,}"
        )

    with c2:
        st.metric(
            "📂 Categories",
            f"{total_categories:,}"
        )

    with c3:
        st.metric(
            "🏟 Complexes",
            f"{total_complexes:,}"
        )

    c4, c5, c6 = st.columns(3)

    with c4:
        st.metric(
            "📍 Venues",
            f"{total_venues:,}"
        )

    with c5:
        st.metric(
            "👤 Competitors",
            f"{total_competitors:,}"
        )

    with c6:
        st.metric(
            "📈 Rankings",
            f"{total_rankings:,}"
        )

    st.divider()

    # =====================================
    # FILTERS
    # =====================================

    left, right = st.columns(2)

    with left:
        top_n = st.selectbox(
            "Top Players",
            [5, 10, 20, 50, 100],
            index=2
        )

    with right:
        ranking_type = st.selectbox(
            "Ranking Type",
            ["All", "ATP", "WTA"]
        )

    # =====================================
    # SINGLE PLAYER QUERY
    # =====================================

    player_df = run_query("""
    SELECT
        c.competitor_name,
        c.country,
        r.rank,
        r.points,
        r.movement,
        r.competitions_played,
        r.ranking_type
    FROM competitor_rankings r
    JOIN competitors c
    ON r.competitor_id = c.competitor_id
    """)

    if ranking_type != "All":

        player_df = player_df[
            player_df["ranking_type"] == ranking_type
        ]

    player_df = player_df.sort_values(
        "rank"
    )

    chart_df = player_df.head(top_n)

    # =====================================
    # HERO SECTION
    # =====================================

    hero_left, hero_right = st.columns([3, 1])

    with hero_left:

        st.subheader(
            "📈 Ranking Points Analysis"
        )

        fig = px.line(
            chart_df,
            x="rank",
            y="points",
            markers=True,
            hover_name="competitor_name"
        )

        fig.update_layout(
            height=450
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with hero_right:

        no1 = player_df.iloc[0]

        st.subheader("🥇 World No.1")

        st.metric(
            "Player",
            no1["competitor_name"]
        )

        st.metric(
            "Country",
            no1["country"]
        )

        st.metric(
            "Rank",
            f"#{no1['rank']}"
        )

        st.metric(
            "Points",
            f"{no1['points']:,}"
        )

    st.divider()
        # =====================================
    # EXECUTIVE SUMMARY QUERY
    # =====================================

    summary_df = run_query("""
    SELECT
        (
            SELECT country
            FROM competitors
            GROUP BY country
            ORDER BY COUNT(*) DESC
            LIMIT 1
        ) AS top_player_country,

        (
            SELECT country_name
            FROM venues
            GROUP BY country_name
            ORDER BY COUNT(*) DESC
            LIMIT 1
        ) AS top_venue_country,

        (
            SELECT MAX(points)
            FROM competitor_rankings
        ) AS highest_points,

        (
            SELECT ROUND(AVG(points),2)
            FROM competitor_rankings
        ) AS avg_points
    """)

    top_player_country = summary_df.iloc[0]["top_player_country"]
    top_venue_country = summary_df.iloc[0]["top_venue_country"]
    highest_points = summary_df.iloc[0]["highest_points"]
    avg_points = summary_df.iloc[0]["avg_points"]

    # =====================================
    # EXECUTIVE SUMMARY
    # =====================================

    st.subheader("📋 Executive Summary")

    e1, e2, e3, e4 = st.columns(4)

    with e1:
        st.metric(
            "🌍 Top Player Country",
            top_player_country
        )

    with e2:
        st.metric(
            "🏟 Top Venue Country",
            top_venue_country
        )

    with e3:
        st.metric(
            "🔥 Highest Points",
            f"{highest_points:,}"
        )

    with e4:
        st.metric(
            "📊 Avg Points",
            f"{avg_points:,}"
        )

    st.divider()

    # =====================================
    # COMPETITION ANALYTICS QUERY
    # =====================================

    competition_type_df = run_query("""
    SELECT
        type,
        COUNT(*) total
    FROM competitions
    GROUP BY type
    ORDER BY total DESC
    """)

    competition_gender_df = run_query("""
    SELECT
        gender,
        COUNT(*) total
    FROM competitions
    GROUP BY gender
    ORDER BY total DESC
    """)

    st.subheader("🏆 Competition Analytics")

    c1, c2 = st.columns(2)

    with c1:

        fig_type = px.bar(
            competition_type_df,
            x="type",
            y="total",
            text="total"
        )

        fig_type.update_layout(
            height=450
        )

        st.plotly_chart(
            fig_type,
            use_container_width=True
        )

    with c2:

        fig_gender = px.pie(
            competition_gender_df,
            names="gender",
            values="total",
            hole=0.5
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
    # VENUE ANALYTICS QUERY
    # =====================================

    venue_country_df = run_query("""
    SELECT
        country_name,
        country_code,
        COUNT(*) total
    FROM venues
    GROUP BY country_name, country_code
    ORDER BY total DESC
    LIMIT 15
    """)

    st.subheader("🌍 Venue Analytics")

    v1, v2 = st.columns(2)

    with v1:

        fig_country = px.bar(
            venue_country_df,
            x="country_name",
            y="total",
            text="total"
        )

        fig_country.update_layout(
            height=500
        )

        st.plotly_chart(
            fig_country,
            use_container_width=True
        )

    with v2:

        fig_map = px.choropleth(
            venue_country_df,
            locations="country_code",
            color="total",
            hover_name="country_name",
            projection="natural earth"
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
    # PLAYER ANALYTICS
    # =====================================

    player_country_df = (
        player_df.groupby("country")
        .size()
        .reset_index(name="total_players")
        .sort_values(
            "total_players",
            ascending=False
        )
        .head(10)
    )

    st.subheader("👤 Player Analytics")

    fig_players = px.bar(
        player_country_df,
        x="country",
        y="total_players",
        text="total_players"
    )

    fig_players.update_layout(
        height=500
    )

    st.plotly_chart(
        fig_players,
        use_container_width=True
    )

    st.divider()

    # =====================================
    # RANKING ANALYTICS
    # =====================================

    st.subheader("📈 Ranking Analytics")

    r1, r2 = st.columns(2)

    with r1:

        fig_hist = px.histogram(
            player_df,
            x="rank",
            nbins=30
        )

        fig_hist.update_layout(
            height=450
        )

        st.plotly_chart(
            fig_hist,
            use_container_width=True
        )

    with r2:

        fig_scatter = px.scatter(
            player_df.head(200),
            x="rank",
            y="points",
            hover_name="competitor_name"
        )

        fig_scatter.update_layout(
            height=450
        )

        st.plotly_chart(
            fig_scatter,
            use_container_width=True
        )

    st.divider()

    # =====================================
    # TOP 10 PLAYERS
    # =====================================

    leaderboard_df = (
        player_df.sort_values("rank")
        .head(10)
        [
            [
                "rank",
                "competitor_name",
                "country",
                "points",
                "movement",
                "competitions_played"
            ]
        ]
    )

    st.subheader("🥇 Top 10 Ranked Players")

    st.dataframe(
        leaderboard_df,
        use_container_width=True,
        hide_index=True,
        height=420
    )

    st.divider()

    # =====================================
    # GAINERS / LOSERS
    # =====================================

    gainers_df = (
        player_df.sort_values(
            "movement",
            ascending=False
        )
        .head(10)
    )

    losers_df = (
        player_df.sort_values(
            "movement",
            ascending=True
        )
        .head(10)
    )

    st.subheader(
        "📊 Ranking Movement Analysis"
    )

    g1, g2 = st.columns(2)

    with g1:

        st.success(
            "🚀 Top Gainers"
        )

        st.dataframe(
            gainers_df[
                [
                    "competitor_name",
                    "country",
                    "rank",
                    "points",
                    "movement"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    with g2:

        st.error(
            "📉 Top Losers"
        )

        st.dataframe(
            losers_df[
                [
                    "competitor_name",
                    "country",
                    "rank",
                    "points",
                    "movement"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    st.divider()

    # =====================================
    # KEY INSIGHTS
    # =====================================

    st.subheader("🎯 Key Insights")

    st.info(
        f"""
• Total Competitions: **{total_competitions:,}**

• Total Venues: **{total_venues:,}**

• Total Competitors: **{total_competitors:,}**

• Total Rankings: **{total_rankings:,}**

• Highest Ranking Points: **{highest_points:,}**

• Top Player Country: **{top_player_country}**

• Top Venue Country: **{top_venue_country}**
"""
    )