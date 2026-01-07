import os
import shutil
import sys
import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.append(str(Path(__file__).resolve().parents[1]))


@pytest.fixture(scope="session", autouse=True)
def _set_test_env():
    temp_root = Path(tempfile.mkdtemp(prefix="creatorstudio_"))
    data_dir = temp_root / "data"
    os.environ["APP_DATA_DIR"] = str(data_dir)
    os.environ["APP_DB_PATH"] = str(data_dir / "app.db")
    os.environ["APP_PROJECTS_DIR"] = str(data_dir / "projects")
    yield
    shutil.rmtree(temp_root, ignore_errors=True)


@pytest.fixture()
def client():
    from app.main import create_app
    from app.db import init_db

    app = create_app()
    init_db()
    return TestClient(app)
