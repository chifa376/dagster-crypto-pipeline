from dagster import Definitions
from dagster_pipeline.assets.extract import crypto_prices_raw
from dagster_pipeline.assets.dbt_assets import crypto_dbt_assets, dbt_resource
from dagster_pipeline.jobs import full_pipeline_job
from dagster_pipeline.schedules import full_pipeline_schedule
from dagster_pipeline.sensors import crypto_sensor

defs = Definitions(
    assets=[crypto_prices_raw, crypto_dbt_assets],
    jobs=[full_pipeline_job],
    schedules=[full_pipeline_schedule],
    sensors=[crypto_sensor],
    resources={
        "dbt": dbt_resource,
    },
)