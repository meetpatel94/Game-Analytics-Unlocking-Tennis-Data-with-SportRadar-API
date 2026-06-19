from db import get_engine
import pandas as pd

print("Connecting...")

engine = get_engine()

print("Connected!")

df = pd.read_sql(
    "SELECT COUNT(*) AS total FROM competitions",
    engine
)

print(df)