import os
import yaml
from pathlib import Path


def load_apis_config():
    """
    Loads 'apis' config from apis.yaml.
    Priority:
    1. Environment variable APIS_CONFIG_PATH
    2. Default path: project_root/airflow/config/apis.yaml
    """
    # 1️⃣ Get path from env var or default
    default_path = Path(__file__).resolve().parents[2] / "airflow" / "config" / "apis.yaml"
    config_path = Path(os.getenv("APIS_CONFIG_PATH", default_path))

    # 2️⃣ Validate path exists
    if not config_path.exists():
        raise FileNotFoundError(
            f"apis.yaml not found.\nTried:\n- {config_path}\n"
            f"Set APIS_CONFIG_PATH env var to override."
        )

    # 3️⃣ Load YAML
    with config_path.open(encoding="utf-8") as f:
        config = yaml.safe_load(f)

    # 4️⃣ Ensure 'apis' key exists
    if "apis" not in config:
        raise KeyError(f"'apis' key not found in {config_path}")

    return config["apis"]

# if __name__ == "__main__":
#     print(load_apis_config())
