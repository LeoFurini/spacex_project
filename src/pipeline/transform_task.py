import json
import tempfile
import logging
from google.cloud import storage
import pandas as pd
from datetime import datetime
from src.utils.gcp_clients import get_storage_client

def transform_raw_to_processed(api_conf, raw_gs_uri):
    """
    Download raw JSON from GCS, normalize it and upload a processed parquet/csv file.
    Returns processed gs:// URI.
    """
    bucket_name = raw_gs_uri.split("/")[2]
    blob_path = "/".join(raw_gs_uri.split("/")[3:])
    client = get_storage_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_path)
    content = blob.download_as_text()
    raw_json = json.loads(content)

    # Use pandas.json_normalize by default — let each API define custom normalizer if needed
    records = raw_json
    # if api returns envelope like {"results": [...]} use config to point to it (not implemented here)
    if isinstance(raw_json, dict) and "results" in raw_json:
        records = raw_json["results"]

    df = pd.json_normalize(records)

    # write to temp file
    fmt = api_conf["output"].get("format", "parquet")
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    processed_prefix = api_conf["output"]["gcs_processed_prefix"].rstrip("/") + "/"
    processed_filename = f"{processed_prefix}{api_conf['name']}_processed_{ts}.{fmt}"

    with tempfile.NamedTemporaryFile(suffix=f".{fmt}", delete=False) as tmp:
        local_path = tmp.name

    if fmt == "parquet":
        df.to_parquet(local_path, index=False)
    elif fmt == "csv":
        df.to_csv(local_path, index=False)
    else:
        raise ValueError("Unsupported format")

    # upload
    proc_blob = bucket.blob(processed_filename)
    proc_blob.upload_from_filename(local_path)
    logging.info(f"Uploaded processed file to gs://{bucket_name}/{processed_filename}")

    # cleanup local file
    import os
    try:
        os.remove(local_path)
    except Exception:
        logging.warning("Could not remove temp file")

    return f"gs://{bucket_name}/{processed_filename}"
