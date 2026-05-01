from dagster import Definitions
from dagster_dbt import DbtCliResource

from dagster_pipeline.assets.extract import crypto_prices_raw
from dagster_pipeline.assets.dbt_assets import (
    crypto_dbt_assets,
    DBT_PROJECT_DIR,
    DBT_PROFILES_DIR,
)

from dagster_pipeline.jobs import crypto_job
from dagster_pipeline.schedules import crypto_schedule
from dagster_pipeline.sensors import crypto_sensor


defs = Definitions(
    assets=[
        crypto_prices_raw,
        crypto_dbt_assets,  
    ],
    jobs=[crypto_job],
    schedules=[crypto_schedule],
    sensors=[crypto_sensor],
    resources={
        "dbt": DbtCliResource(
            project_dir=DBT_PROJECT_DIR,
            profiles_dir=DBT_PROFILES_DIR,
        )
    },
)