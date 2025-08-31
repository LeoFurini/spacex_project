import logging
from google.cloud import bigquery
from src.utils.gcp_clients import get_bigquery_client

def load_processed_to_bq(api_conf, processed_gs_uri):
    """
    Load file at processed_gs_uri into BigQuery table specified in api_conf.
    """
    bq_conf = api_conf["bigquery"]
    dataset = bq_conf["dataset"]
    table = bq_conf["table"]
    destination = f"{dataset}.{table}"

    client = get_bigquery_client()
    job_config = bigquery.LoadJobConfig(
        autodetect=True,
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
    )
    if processed_gs_uri.endswith(".parquet"):
        job_config.source_format = bigquery.SourceFormat.PARQUET
    else:
        job_config.source_format = bigquery.SourceFormat.CSV
        job_config.skip_leading_rows = 1

    logging.info(f"Starting BQ load of {processed_gs_uri} -> {destination}")
    load_job = client.load_table_from_uri(processed_gs_uri, destination, job_config=job_config)
    load_job.result()
    logging.info("BigQuery load finished")
    return True
