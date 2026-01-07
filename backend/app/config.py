from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = Path(os.getenv("APP_DATA_DIR", str(BASE_DIR / "data")))
DB_PATH = Path(os.getenv("APP_DB_PATH", str(DATA_DIR / "app.db")))
PROJECTS_DIR = Path(os.getenv("APP_PROJECTS_DIR", str(DATA_DIR / "projects")))
SETTINGS_PATH = Path(os.getenv("APP_SETTINGS_PATH", str(DATA_DIR / "settings.json")))


def ensure_dirs() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    PROJECTS_DIR.mkdir(parents=True, exist_ok=True)
