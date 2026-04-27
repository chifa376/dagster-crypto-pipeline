from dagster import ScheduleDefinition
from dagster_pipeline.jobs import crypto_job

crypto_schedule = ScheduleDefinition(
    job=crypto_job,
    cron_schedule="0 * * * *",  # chaque heure
)