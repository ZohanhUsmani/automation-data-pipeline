"""Validation helpers returning (ok, errors)."""
import re
import pandas as pd


class ValidationError(Exception):
    pass


def require_columns(df: pd.DataFrame, required) -> list[str]:
    missing = [c for c in required if c not in df.columns]
    return missing


def check_not_null(df: pd.DataFrame, columns) -> list[str]:
    errs = []
    for col in columns:
        if col in df.columns and df[col].isna().any():
            n = int(df[col].isna().sum())
            errs.append(f"column '{col}' has {n} null value(s)")
    return errs


def check_range(df: pd.DataFrame, column, min_val=None, max_val=None) -> list[str]:
    errs = []
    if column not in df.columns:
        return errs
    if min_val is not None and (df[column] < min_val).any():
        errs.append(f"column '{column}' has values below {min_val}")
    if max_val is not None and (df[column] > max_val).any():
        errs.append(f"column '{column}' has values above {max_val}")
    return errs


def check_regex(df: pd.DataFrame, column, pattern) -> list[str]:
    errs = []
    if column not in df.columns:
        return errs
    rx = re.compile(pattern)
    bad = df[column].astype(str).apply(lambda v: rx.fullmatch(v) is None)
    if bad.any():
        errs.append(f"column '{column}' has {int(bad.sum())} value(s) not matching {pattern}")
    return errs


def validate(df: pd.DataFrame, rules: dict) -> list[str]:
    errors = []
    errors.extend([f"missing required column: {c}" for c in require_columns(df, rules.get("required", []))])
    errors.extend(check_not_null(df, rules.get("not_null", [])))
    for col, (mn, mx) in rules.get("ranges", {}).items():
        errors.extend(check_range(df, col, mn, mx))
    for col, pat in rules.get("regex", {}).items():
        errors.extend(check_regex(df, col, pat))
    return errors