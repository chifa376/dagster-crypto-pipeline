from dagster import define_asset_job

crypto_job = define_asset_job(
    name="crypto_job",
    selection=["crypto_prices_raw"]
)