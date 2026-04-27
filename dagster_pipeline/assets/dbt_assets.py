from dagster_dbt import dbt_assets, DbtCliResource

dbt_resource = DbtCliResource(
    project_dir="dbt_project/crypto_pipeline",
)

@dbt_assets(manifest="dbt_project/crypto_pipeline/target/manifest.json")
def crypto_dbt_assets(context, dbt: DbtCliResource):
    yield from dbt.cli(["run"], context=context).stream()