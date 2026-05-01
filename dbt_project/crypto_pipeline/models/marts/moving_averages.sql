select
    coin_id,
    symbol,
    name,
    price_date,
    avg_price,

    avg(avg_price) over (
        partition by coin_id
        order by price_date
        rows between 6 preceding and current row
    ) as moving_avg_7d

from {{ ref('daily_summary') }}