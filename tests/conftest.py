import os
import tempfile
import shutil
import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="session")
def tmp_dir(tmp_path_factory):
    d = tmp_path_factory.mktemp("data")
    yield d


@pytest.fixture(scope="function")
def client(tmp_dir, monkeypatch):
    # if TEST_USE_POSTGRES is set, tests will use DATABASE_URL from env (CI)
    use_postgres = bool(os.getenv("TEST_USE_POSTGRES"))
    if use_postgres:
        db_url = os.getenv("DATABASE_URL")
    else:
        # use a file-based sqlite DB per test to avoid threading issues
        db_file = tmp_dir / "test.db"
        db_url = f"sqlite:///{db_file}"
        # set env var so app.db will read correct URL if imported later
        monkeypatch.setenv("DATABASE_URL", db_url)

    # import here so modules pick up monkeypatched env
    from app import main
    from app.db import override_database, init_db

    override_database(db_url)
    init_db()

    client = TestClient(main.app)
    yield client

    # cleanup sqlite DB if used
    if not use_postgres:
        try:
            if db_file.exists():
                db_file.unlink()
        except Exception:
            pass
