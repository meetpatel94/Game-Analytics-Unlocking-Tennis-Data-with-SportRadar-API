import os
import json
from pathlib import Path
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# =====================================================
# NEON DATABASE URL
# =====================================================

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError(
        "❌ DATABASE_URL not found in .env file"
    )

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

# =====================================================
# TEST CONNECTION
# =====================================================

print("=" * 60)
print("TESTING DATABASE CONNECTION")
print("=" * 60)

with engine.connect() as conn:
    print("Database Connected:", conn.execute(text("SELECT 1")).scalar())

# =====================================================
# FILE PATHS
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

COMPETITIONS_FILE = BASE_DIR / "data" / "competitions.json"
COMPLEXES_FILE = BASE_DIR / "data" / "complexes.json"
RANKINGS_FILE = BASE_DIR / "data" / "double_competitors_rankings.json"

# =====================================================
# LOAD JSON FILES
# =====================================================

print("\nLoading JSON Files...")

with open(COMPETITIONS_FILE, "r", encoding="utf-8") as f:
    competitions_data = json.load(f)

with open(COMPLEXES_FILE, "r", encoding="utf-8") as f:
    complexes_data = json.load(f)

with open(RANKINGS_FILE, "r", encoding="utf-8") as f:
    rankings_data = json.load(f)

print("Competitions:", len(competitions_data["competitions"]))
print("Complexes:", len(complexes_data["complexes"]))
print("Ranking Groups:", len(rankings_data["rankings"]))

# =====================================================
# IMPORT CATEGORIES + COMPETITIONS
# =====================================================

print("\nIMPORTING CATEGORIES & COMPETITIONS")

inserted_categories = set()

with engine.begin() as conn:

    for idx, comp in enumerate(competitions_data["competitions"], start=1):

        category = comp.get("category", {})

        cat_id = category.get("id")
        cat_name = category.get("name")

        if cat_id and cat_id not in inserted_categories:

            conn.execute(
                text("""
                INSERT INTO categories
                (category_id, category_name)
                VALUES
                (:id, :name)
                ON CONFLICT (category_id) DO NOTHING
                """),
                {
                    "id": cat_id,
                    "name": cat_name
                }
            )

            inserted_categories.add(cat_id)

        conn.execute(
            text("""
            INSERT INTO competitions
            (
                competition_id,
                competition_name,
                parent_id,
                type,
                gender,
                category_id
            )
            VALUES
            (
                :competition_id,
                :competition_name,
                :parent_id,
                :type,
                :gender,
                :category_id
            )
            ON CONFLICT (competition_id) DO NOTHING
            """),
            {
                "competition_id": comp.get("id"),
                "competition_name": comp.get("name"),
                "parent_id": comp.get("parent_id"),
                "type": comp.get("type"),
                "gender": comp.get("gender"),
                "category_id": cat_id
            }
        )

        if idx % 500 == 0:
            print(f"Competitions Imported: {idx}")

print("Competitions Import Completed")

# =====================================================
# IMPORT COMPLEXES + VENUES
# =====================================================

print("\nIMPORTING COMPLEXES & VENUES")

venue_count = 0

with engine.begin() as conn:

    for idx, complex_item in enumerate(complexes_data["complexes"], start=1):

        complex_id = complex_item.get("id")

        conn.execute(
            text("""
            INSERT INTO complexes
            (
                complex_id,
                complex_name
            )
            VALUES
            (
                :complex_id,
                :complex_name
            )
            ON CONFLICT (complex_id) DO NOTHING
            """),
            {
                "complex_id": complex_id,
                "complex_name": complex_item.get("name")
            }
        )

        for venue in complex_item.get("venues", []):

            venue_count += 1

            conn.execute(
                text("""
                INSERT INTO venues
                (
                    venue_id,
                    venue_name,
                    city_name,
                    city_id,
                    country_name,
                    country_code,
                    timezone,
                    complex_id
                )
                VALUES
                (
                    :venue_id,
                    :venue_name,
                    :city_name,
                    :city_id,
                    :country_name,
                    :country_code,
                    :timezone,
                    :complex_id
                )
                ON CONFLICT (venue_id) DO NOTHING
                """),
                {
                    "venue_id": venue.get("id"),
                    "venue_name": venue.get("name"),
                    "city_name": venue.get("city_name"),
                    "city_id": venue.get("city_id"),
                    "country_name": venue.get("country_name"),
                    "country_code": venue.get("country_code"),
                    "timezone": venue.get("timezone"),
                    "complex_id": complex_id
                }
            )

        if idx % 100 == 0:
            print(f"Complexes Imported: {idx}")

print("Complexes Import Completed")
print("Total Venues:", venue_count)

# =====================================================
# IMPORT COMPETITORS + RANKINGS
# =====================================================

print("\nIMPORTING COMPETITORS & RANKINGS")

ranking_count = 0

with engine.begin() as conn:

    for ranking_group in rankings_data["rankings"]:

        ranking_type = ranking_group.get("name")
        ranking_year = ranking_group.get("year")
        ranking_week = ranking_group.get("week")
        gender = ranking_group.get("gender")

        for item in ranking_group["competitor_rankings"]:

            competitor = item["competitor"]

            competitor_id = competitor.get("id")

            conn.execute(
                text("""
                INSERT INTO competitors
                (
                    competitor_id,
                    competitor_name,
                    country,
                    country_code,
                    abbreviation
                )
                VALUES
                (
                    :competitor_id,
                    :competitor_name,
                    :country,
                    :country_code,
                    :abbreviation
                )
                ON CONFLICT (competitor_id) DO NOTHING
                """),
                {
                    "competitor_id": competitor_id,
                    "competitor_name": competitor.get("name"),
                    "country": competitor.get("country"),
                    "country_code": competitor.get("country_code"),
                    "abbreviation": competitor.get("abbreviation")
                }
            )

            conn.execute(
                text("""
                INSERT INTO competitor_rankings
                (
                    rank,
                    movement,
                    points,
                    competitions_played,
                    ranking_type,
                    ranking_year,
                    ranking_week,
                    gender,
                    competitor_id
                )
                VALUES
                (
                    :rank,
                    :movement,
                    :points,
                    :competitions_played,
                    :ranking_type,
                    :ranking_year,
                    :ranking_week,
                    :gender,
                    :competitor_id
                )
                """),
                {
                    "rank": item.get("rank"),
                    "movement": item.get("movement"),
                    "points": item.get("points"),
                    "competitions_played": item.get("competitions_played"),
                    "ranking_type": ranking_type,
                    "ranking_year": ranking_year,
                    "ranking_week": ranking_week,
                    "gender": gender,
                    "competitor_id": competitor_id
                }
            )

            ranking_count += 1

            if ranking_count % 500 == 0:
                print(f"Rankings Imported: {ranking_count}")

print("Rankings Import Completed")

print("\n" + "=" * 60)
print("DATABASE IMPORT COMPLETED SUCCESSFULLY")
print("=" * 60)
