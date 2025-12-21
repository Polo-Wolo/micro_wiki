import yaml
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = BASE_DIR / "config.yml"

_CONFIG = {}

def load_config():
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"config.yml manquant ({CONFIG_PATH})")

    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f) or {}

    config.setdefault("site", {})
    config.setdefault("paths", {})

    # Résolution chemins
    notes_rel = config["paths"].get("notes", "notes")
    config["paths"]["notes"] = (BASE_DIR / notes_rel).resolve()

    return config

def get_config():
    if not _CONFIG:
        _CONFIG.update(load_config())
    return _CONFIG

def reload_config():
    _CONFIG.clear()
    _CONFIG.update(load_config())
