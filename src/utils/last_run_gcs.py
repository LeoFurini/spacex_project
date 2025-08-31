import json
from google.cloud import storage
from datetime import datetime
import logging

def _blob(client, bucket_name, api_name):
    return client.bucket(bucket_name).blob(f"state/{api_name}_last_run.json")

def get_last_run(bucket_name, api_name):
    client = storage.Client()
    blob = _blob(client, bucket_name, api_name)
    if blob.exists():
        try:
            content = blob.download_as_text()
            payload = json.loads(content)
            return payload.get("last_run")
        except Exception:
            logging.exception("Failed reading last_run blob")
            return None
    return None

def set_last_run(bucket_name, api_name, last_run_value=None):
    client = storage.Client()
    blob = _blob(client, bucket_name, api_name)
    if last_run_value is None:
        last_run_value = datetime.utcnow().isoformat()
    blob.upload_from_string(json.dumps({"last_run": last_run_value}), content_type="application/json")
    return last_run_value
