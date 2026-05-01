import requests
import pandas as pd
from dagster import asset
from dagster_pipeline.resources.database import get_connection


@asset
def crypto_prices_raw():
    url = "https://api.coingecko.com/api/v3/simple/price"

    params = {
        "ids": "bitcoin,ethereum,solana",
        "vs_currencies": "usd,eur",
        "include_market_cap": "true",
        "include_24hr_change": "true",
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()

    rows = []
    for crypto, values in data.items():
        rows.append({
            "crypto": crypto,
            "price_usd": values.get("usd"),
            "price_eur": values.get("eur"),
            "market_cap_usd": values.get("usd_market_cap"),
            "change_24h_usd": values.get("usd_24h_change"),
            "extracted_at": pd.Timestamp.now(),
        })

    df = pd.DataFrame(rows)

    conn = get_connection()

    # 1. créer la table si elle n'existe pas
    conn.execute("""
        CREATE TABLE IF NOT EXISTS crypto_prices_raw (
            crypto VARCHAR,
            price_usd DOUBLE,
            price_eur DOUBLE,
            market_cap_usd DOUBLE,
            change_24h_usd DOUBLE,
            extracted_at TIMESTAMP
        )
    """)

    # 2. ajouter les nouvelles données (sans supprimer l'ancien)
    conn.execute("INSERT INTO crypto_prices_raw SELECT * FROM df")

    conn.close()

    return df