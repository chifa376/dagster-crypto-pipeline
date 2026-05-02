import duckdb
from dagster_pipeline.assets.extract import crypto_prices_raw

DB_PATH = "data/crypto.duckdb"


def test_crypto_prices_raw_creates_table_and_data():
    crypto_prices_raw()

    conn = duckdb.connect(DB_PATH)

    tables = conn.execute("SHOW TABLES").fetchdf()["name"].tolist()
    count = conn.execute("SELECT COUNT(*) FROM crypto_prices_raw").fetchone()[0]

    columns = conn.execute("DESCRIBE crypto_prices_raw").fetchdf()["column_name"].tolist()

    invalid_prices = conn.execute("""
        SELECT COUNT(*)
        FROM crypto_prices_raw
        WHERE price_usd <= 0
           OR price_eur <= 0
           OR market_cap_usd <= 0
    """).fetchone()[0]

    conn.close()

    assert "crypto_prices_raw" in tables
    assert count > 0
    assert "crypto" in columns
    assert "price_usd" in columns
    assert "price_eur" in columns
    assert "market_cap_usd" in columns
    assert "change_24h_usd" in columns
    assert "extracted_at" in columns
    assert invalid_prices == 0