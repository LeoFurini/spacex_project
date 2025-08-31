import json
import logging
from datetime import datetime
from src.extract.api_client_base import fetch_api_json
from src.utils.gcp_clients import get_storage_client
from src.utils.last_run_gcs import get_last_run, set_last_run
from src.utils.config import GCS_BUCKET

def extract_and_save_raw(api_conf):
    """
    Fetch API and upload raw JSON to GCS. Also returns the GCS URI for the raw file.
    """
    api_name = api_conf["name"]
    # get last_run (if incremental)
    last_run = None
    if api_conf.get("incremental", {}).get("enabled", False):
        last_run = get_last_run(GCS_BUCKET, api_name)

    data = fetch_api_json(api_conf, since_value=last_run)

    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    raw_prefix = api_conf["output"]["gcs_raw_prefix"].rstrip("/") + "/"
    raw_filename = f"{raw_prefix}{api_name}_raw_{ts}.json"
    client = get_storage_client()
    bucket = client.bucket(GCS_BUCKET)
    blob = bucket.blob(raw_filename)
    blob.upload_from_string(json.dumps(data), content_type="application/json")
    logging.info(f"Uploaded raw JSON to gs://{GCS_BUCKET}/{raw_filename}")

    # update last_run using server/now (you might prefer using max(updated_at) from data)
    new_last_run = set_last_run(GCS_BUCKET, api_name)
    return f"gs://{GCS_BUCKET}/{raw_filename}"


# if __name__ == "__main__":
#     print(extract_and_save_raw())