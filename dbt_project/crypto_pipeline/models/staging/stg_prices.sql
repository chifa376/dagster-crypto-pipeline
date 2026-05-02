select
    crypto,
    price_usd,
    price_eur,
    market_cap_usd,
    change_24h_usd,
    extracted_at
from {{ source('raw', 'crypto_prices_raw') }}