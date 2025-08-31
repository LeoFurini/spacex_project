import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import logging

def requests_session_with_retries(total_retries=3, backoff_factor=0.5, status_forcelist=(429, 500, 502, 503, 504)):
    session = requests.Session()
    retries = Retry(total=total_retries, backoff_factor=backoff_factor, status_forcelist=status_forcelist, allowed_methods=["GET", "POST"])
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session

def fetch_api_json(api_conf, since_value=None):
    """
    Fetch JSON from API according to configuration.
    Returns the parsed JSON (Python object).
    """
    session = requests_session_with_retries()
    headers = {}
    params = dict(api_conf.get("params", {}))

    auth = api_conf.get("auth", {})
    if auth.get("type") == "bearer":
        token = __import__("os").environ.get(auth.get("token_env"))
        headers["Authorization"] = f"Bearer {token}"
    elif auth.get("type") == "api_key":
        key = __import__("os").environ.get(auth.get("key_env"))
        # put key in headers or params depending on config
        if auth.get("key_in") == "header":
            headers[auth.get("key_header", "x-api-key")] = key
        else:
            params[auth.get("key_param", "apikey")] = key

    # incremental
    inc = api_conf.get("incremental", {})
    if since_value and inc.get("enabled"):
        params[inc.get("since_param", "since")] = since_value

    url = api_conf["base_url"].rstrip("/") + api_conf["endpoint"]
    logging.info(f"Fetching URL: {url} params={params}")
    r = session.get(url, headers=headers, params=params, timeout=60)
    r.raise_for_status()
    return r.json()
