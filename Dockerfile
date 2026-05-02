FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN cd dbt_project/crypto_pipeline && dbt parse

EXPOSE 3000
EXPOSE 8501

CMD ["dagster", "dev", "-m", "dagster_pipeline.definitions", "-h", "0.0.0.0"]