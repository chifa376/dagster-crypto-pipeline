SELECT
    crypto,
    AVG(price_usd) AS avg_price_usd,
    AVG(change_24h_usd) AS avg_change,
    COUNT(*) AS nb_records
FROM crypto_prices_raw
GROUP BY crypto