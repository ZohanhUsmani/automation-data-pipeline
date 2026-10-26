"""Export helpers."""
import json
from datetime import datetime
from pathlib import Path
import pandas as pd


def _stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def to_csv(df: pd.DataFrame, path: Path) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    out = path if path.suffix else path / f"output_{_stamp()}.csv"
    if out.is_dir():
        out = out / f"output_{_stamp()}.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False)
    return out


def to_excel(df: pd.DataFrame, path: Path) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    out = path if path.suffix else path / f"output_{_stamp()}.xlsx"
    if out.is_dir():
        out = out / f"output_{_stamp()}.xlsx"
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_excel(out, index=False)
    return out


def to_json(df: pd.DataFrame, path: Path) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    out = path if path.suffix else path / f"output_{_stamp()}.json"
    if out.is_dir():
        out = out / f"output_{_stamp()}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(df.to_dict(orient="records"), f, indent=2, default=str)
    return out