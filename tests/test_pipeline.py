from src.pipeline import run
import tempfile, os
from pathlib import Path


def test_end_to_end(tmp_path):
    inp = Path("data/sample_input.csv")
    out = run(inp, tmp_path, "csv", {"cleaning": {"numeric_columns": ["age", "salary"]},
                                     "validation": {"required": ["name", "age", "email"]}})
    assert out.exists()