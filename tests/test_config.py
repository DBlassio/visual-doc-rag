from docrag import config


def test_data_dirs_live_under_repo_by_default(monkeypatch):
    monkeypatch.delenv("DOCRAG_DATA_DIR", raising=False)
    assert config.raw_dir() == config.REPO_ROOT / "data" / "raw"
    assert config.pages_dir() == config.REPO_ROOT / "data" / "pages"


def test_data_dir_override(monkeypatch, tmp_path):
    monkeypatch.setenv("DOCRAG_DATA_DIR", str(tmp_path))
    assert config.data_dir() == tmp_path
