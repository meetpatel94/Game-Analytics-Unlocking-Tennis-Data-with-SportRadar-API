from queries.query import run_query

df = run_query("""
SELECT *
FROM competitions
LIMIT 5
""")

print(df)