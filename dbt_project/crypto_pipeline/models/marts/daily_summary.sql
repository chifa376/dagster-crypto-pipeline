select
    coin_id,
    symbol,
    name,
    date(last_updated) as price_date,

    avg(current_price) as avg_price,
    min(current_price) as min_price,
    max(current_price) as max_price,

    avg(total_volume) as avg_volume,
    avg(market_cap) as avg_market_cap

from {{ ref('stg_prices') }}

group by coin_id, symbol, name, date(last_updated)