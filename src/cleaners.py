"""Data cleaning helpers."""
import re
import pandas as pd


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [re.sub(r"\s+", "_", str(c).strip().lower()) for c in df.columns]
    return df


def trim_strings(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype(str).str.strip()
    return df


def drop_duplicates(df: pd.DataFrame, subset=None) -> pd.DataFrame:
    return df.drop_duplicates(subset=subset).reset_index(drop=True)


def coerce_numeric(df: pd.DataFrame, columns) -> pd.DataFrame:
    df = df.copy()
    for col in columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def fill_missing(df: pd.DataFrame, strategy: str = "none", value=None) -> pd.DataFrame:
    df = df.copy()
    if strategy == "drop":
        return df.dropna().reset_index(drop=True)
    if strategy == "value":
        return df.fillna(value)
    if strategy == "mean":
        for col in df.select_dtypes(include="number").columns:
            df[col] = df[col].fillna(df[col].mean())
        return df
    return df