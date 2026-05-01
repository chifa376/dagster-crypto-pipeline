select
    crypto,
    price_usd,
    avg(price_usd) over (
        partition by crypto
        order by price_usd
        rows between 2 preceding and current row
    ) as moving_avg_3

from {{ ref('stg_prices') }}