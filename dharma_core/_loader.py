from importlib.resources import files
from pathlib import Path
from typing import Iterator, Dict, Any, List
import io
import json
import yaml
import pandas as pd

SCHEMA_VERSION = "1.0"

def _pkg_path(*parts: str) -> Path:
    # returns a Traversable-like object that supports read_text/read_bytes
    return files(__package__).joinpath(*parts)

def package_root() -> Path:
    return _pkg_path("artifacts")  # type: ignore[return-value]

def list_artifacts() -> Dict[str, List[str]]:
    # Lightweight manifest by directory
    result = {}
    for d in ["scrolls", "simulations", "mirror", "memory"]:
        base = _pkg_path("artifacts", d)
        if not base.is_dir():
            continue
        names = [p.name for p in base.iterdir() if p.is_file()]
        result[d] = sorted(names)
    return result

def _iter_yaml(subdir: str) -> Iterator[Dict[str, Any]]:
    base = _pkg_path("artifacts", subdir)
    if not base.is_dir():
        return iter(())
    def gen() -> Iterator[Dict[str, Any]]:
        for p in base.iterdir():
            n = p.name.lower()
            if n.endswith((".yaml", ".yml")):
                yield yaml.safe_load(p.read_text(encoding="utf-8"))
    return gen()

def load_scrolls() -> List[Dict[str, Any]]:
    return list(_iter_yaml("scrolls"))

def iter_simulations() -> Iterator[Dict[str, Any]]:
    return _iter_yaml("simulations")

def load_verse_matrix(csv_name: str = "verse_matrix.csv") -> pd.DataFrame:
    # Looks under artifacts/data/ by default; map your CSV into that path in pyproject
    data_dir = _pkg_path("artifacts", "data")
    target = data_dir.joinpath(csv_name)
    with target.open("rb") as fh:
        return pd.read_csv(io.BytesIO(fh.read()))

def get_manifest() -> Dict[str, Any]:
    # If you keep a generated manifest.json under memory/ or specs/, this will surface it.
    for candidate in [
        _pkg_path("artifacts", "memory", "manifest.json"),
        _pkg_path("specs", "schemas", "manifest.json"),
    ]:
        if candidate.is_file():
            return json.loads(candidate.read_text(encoding="utf-8"))
    return {
        "schema_version": SCHEMA_VERSION,
        "artifacts": list_artifacts(),
    }
