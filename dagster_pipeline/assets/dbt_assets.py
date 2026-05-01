from pathlib import Path

from dagster import AssetExecutionContext
from dagster_dbt import DbtCliResource, dbt_assets

DBT_PROJECT_DIR = Path(__file__).joinpath(
    "..", "..", "..", "dbt_project", "crypto_pipeline"
).resolve()

DBT_PROFILES_DIR = DBT_PROJECT_DIR
DBT_MANIFEST_PATH = DBT_PROJECT_DIR / "target" / "manifest.json"


@dbt_assets(manifest=DBT_MANIFEST_PATH)
def crypto_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()