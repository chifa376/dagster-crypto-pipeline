import duckdb

conn = duckdb.connect("data/crypto.duckdb")

print("=== crypto_prices_raw ===")
df = conn.execute("""
    SELECT *
    FROM crypto_prices_raw
""").fetchdf()
print(df)

print("=== daily_summary ===")
df = conn.execute("""
    SELECT *
    FROM daily_summary
""").fetchdf()
print(df)

conn.close()