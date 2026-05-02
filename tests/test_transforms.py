import duckdb

DB_PATH = "data/crypto.duckdb"


def get_tables():
    conn = duckdb.connect(DB_PATH)
    tables = conn.execute("SHOW TABLES").fetchdf()["name"].tolist()
    conn.close()
    return tables


def test_dbt_transformed_tables_exist():
    tables = get_tables()

    assert "daily_summary" in tables
    assert "moving_averages" in tables


def test_daily_summary_quality():
    conn = duckdb.connect(DB_PATH)

    count = conn.execute("SELECT COUNT(*) FROM daily_summary").fetchone()[0]
    columns = conn.execute("DESCRIBE daily_summary").fetchdf()["column_name"].tolist()

    invalid_values = conn.execute("""
        SELECT COUNT(*)
        FROM daily_summary
        WHERE avg_price_usd <= 0
           OR avg_price_eur <= 0
           OR avg_market_cap_usd <= 0
           OR nb_records <= 0
    """).fetchone()[0]

    conn.close()

    assert count > 0
    assert "crypto" in columns
    assert "avg_price_usd" in columns
    assert "avg_price_eur" in columns
    assert "avg_market_cap_usd" in columns
    assert "avg_change" in columns
    assert "nb_records" in columns
    assert invalid_values == 0


def test_moving_averages_quality():
    conn = duckdb.connect(DB_PATH)

    count = conn.execute("SELECT COUNT(*) FROM moving_averages").fetchone()[0]
    columns = conn.execute("DESCRIBE moving_averages").fetchdf()["column_name"].tolist()

    invalid_values = conn.execute("""
        SELECT COUNT(*)
        FROM moving_averages
        WHERE price_usd <= 0
           OR moving_avg_3 <= 0
    """).fetchone()[0]

    conn.close()

    assert count > 0
    assert "crypto" in columns
    assert "price_usd" in columns
    assert "moving_avg_3" in columns
    assert invalid_values == 0