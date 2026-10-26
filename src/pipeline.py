"""Main data pipeline orchestrator."""
import argparse
import time
from pathlib import Path

import pandas as pd
import yaml

from .cleaners import (normalize_columns, trim_strings, drop_duplicates,
                       coerce_numeric, fill_missing)
from .validators import validate
from .exporters import to_csv, to_excel, to_json
from .logger import get_logger

log = get_logger()


def read_input(path: Path) -> pd.DataFrame:
    path = Path(path)
    if path.suffix.lower() in (".xlsx", ".xls"):
        return pd.read_excel(path)
    return pd.read_csv(path)


def run(input_path, output_dir, fmt="csv", config=None):
    config = config or {}
    cleaning = config.get("cleaning", {})
    validation = config.get("validation", {})

    log.info("Reading input: %s", input_path)
    df = read_input(Path(input_path))
    log.info("Loaded %d rows, %d cols", len(df), len(df.columns))

    df = normalize_columns(df)
    df = trim_strings(df)
    if cleaning.get("drop_duplicates", True):
        before = len(df)
        df = drop_duplicates(df)
        log.info("Dropped %d duplicate rows", before - len(df))
    for col in cleaning.get("numeric_columns", []):
        df = coerce_numeric(df, [col])
    df = fill_missing(df, strategy=cleaning.get("fill_strategy", "none"),
                      value=cleaning.get("fill_value"))

    errors = validate(df, validation)
    if errors:
        for e in errors:
            log.error("Validation: %s", e)
        raise ValueError("; ".join(errors))
    log.info("Validation passed")

    transform = config.get("transform") or {}
    if "filter" in transform:
        expr = transform["filter"]
        df = df.query(expr)
        log.info("After filter: %d rows", len(df))

    out_dir = Path(output_dir)
    if fmt == "csv":
        out = to_csv(df, out_dir)
    elif fmt == "excel":
        out = to_excel(df, out_dir)
    elif fmt == "json":
        out = to_json(df, out_dir)
    else:
        raise ValueError(f"unknown format {fmt}")
    log.info("Exported to %s", out)
    return out


def main():
    ap = argparse.ArgumentParser(description="Data cleaning pipeline")
    ap.add_argument("--input", required=True, help="input CSV/XLSX path")
    ap.add_argument("--output", default="out", help="output directory")
    ap.add_argument("--format", default="csv", choices=["csv", "excel", "json"])
    ap.add_argument("--config", default=None, help="YAML config path")
    args = ap.parse_args()

    cfg = {}
    if args.config and Path(args.config).exists():
        with open(args.config) as f:
            cfg = yaml.safe_load(f) or {}

    t0 = time.time()
    try:
        out = run(args.input, args.output, args.format, cfg)
        log.info("Done in %.2fs -> %s", time.time() - t0, out)
    except Exception as e:
        log.exception("Pipeline failed: %s", e)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
