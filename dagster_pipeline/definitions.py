from dagster import Definitions
from dagster_pipeline.assets.extract import crypto_prices_raw
from dagster_pipeline.jobs import crypto_job
from dagster_pipeline.schedules import crypto_schedule
from dagster_pipeline.sensors import crypto_sensor

defs = Definitions(
    assets=[crypto_prices_raw],
    jobs=[crypto_job],
    schedules=[crypto_schedule],
    sensors=[crypto_sensor],
)