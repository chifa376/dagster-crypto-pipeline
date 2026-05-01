from dagster import ScheduleDefinition
from dagster_pipeline.jobs import full_pipeline_job

full_pipeline_schedule = ScheduleDefinition(
    job=full_pipeline_job,
    cron_schedule="*/5 * * * *",  # toutes les 5 min
)