from pathlib import Path
from dagster import sensor, RunRequest, SkipReason
from dagster_pipeline.jobs import crypto_job

TRIGGER_FILE = Path("triggers/run_crypto.txt")


@sensor(job=crypto_job)
def crypto_sensor():
    if TRIGGER_FILE.exists():
        TRIGGER_FILE.unlink()

        return RunRequest(
            run_key=None,
            run_config={}
        )

    return SkipReason("Aucun fichier trigger trouvé.")