from pathlib import Path
from dagster import sensor, RunRequest, SkipReason
from dagster_pipeline.jobs import crypto_job

TRIGGER_FILE = Path("triggers/run_crypto.txt")

from dagster import DailyPartitionsDefinition

daily_partitions = DailyPartitionsDefinition(start_date="2024-01-01")
@sensor(job=crypto_job)
def crypto_sensor():
    if TRIGGER_FILE.exists():
        TRIGGER_FILE.unlink()

        return RunRequest(
            run_key=None,
            run_config={}
        )

    return SkipReason("Aucun fichier trigger trouvé.")