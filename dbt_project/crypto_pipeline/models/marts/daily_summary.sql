select
    crypto,
    avg(price_usd) as avg_price_usd,
    avg(price_eur) as avg_price_eur,
    avg(market_cap_usd) as avg_market_cap_usd,
    avg(change_24h_usd) as avg_change,
    count(*) as nb_records

from {{ ref('stg_prices') }}

group by crypto