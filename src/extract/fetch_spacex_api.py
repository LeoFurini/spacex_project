##Importar os pacotes
import requests
import pandas as pd
import logging
from google.cloud import storage
from datetime import datetime

#BUCKET_NAME = "spacex-raw-data"  # your GCS bucket
FILE_FORMAT = "csv"              # or "parquet"
FILE_NAME = f"spacex_launches_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.{FILE_FORMAT}"
DESTINATION_BLOB_NAME = f"raw/{FILE_NAME}"  # path inside GCS bucket

# Make sure this env var is set to your service account file path
# export GOOGLE_APPLICATION_CREDENTIALS="/path/to/spacex-ingestor-key.json"

# ================== Logging ==================
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


# ================ Extract ===================
def extract_from_spacex():
    url = "https://api.spacexdata.com/v4/launches"
    try:
        response = requests.get(url)
        response.raise_for_status()
        logging.info("✅ Successfully fetched launch data from SpaceX API")
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"❌ Failed to fetch data: {e}")
    return []

result = extract_from_spacex();
display(result);

-- Estudar sobre formas de requistar API e como escrever codigo Python para isso?
-- Estudar como manipular as variaveis de uma requisição de API extraindo os campos que quero usar?
-- 

Conectar na API e puxar = Extrair
?????
Joga pro GCS = Load

Fazer a conexão da api com o GCS - Google Cloud Storage
